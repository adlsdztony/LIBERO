import os
from typing import List
from anthropic import AnthropicBedrock
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def png_to_base64(png_path: str):
    """Convert a PNG file to a base64-encoded string."""
    import base64
    with open(png_path, "rb") as png_file:
        return base64.b64encode(png_file.read()).decode('utf-8')

def even_sample_indices(total, desired):
    """
    Evenly sample `desired` indices from a list of length `total`.
    Always include the first and last elements.
    """
    if desired >= total:
        return list(range(total))
    elif desired == 1:
        return [total-1]
    elif desired == 2:
        return [0, total-1]
    else:
        import numpy as np
        # Always pick the first and last, evenly sample the rest
        idx = np.linspace(1, total-2, num=desired-2, dtype=int).tolist()
        return [0] + idx + [total-1]

def extract_openai_output(response):
    """
    Extracts the main output text and reasoning summaries from an OpenAI-style response object.
    Concatenates them, labeling the reasoning section if present.

    Args:
        response: The response object returned by the OpenAI API.

    Returns:
        str: The combined main output text and reasoning text, or stringified response if extraction fails.
    """
    main_texts = []
    reasoning_texts = []

    # Extract from response.output (which is a list)
    output_list = getattr(response, "output", None)
    if isinstance(output_list, list):
        for item in output_list:
            # Extract reasoning summaries
            if getattr(item, "type", None) == "reasoning":
                summary_list = getattr(item, "summary", [])
                if isinstance(summary_list, list):
                    for summary_obj in summary_list:
                        # Try .text attribute or 'text' key if it's a dict
                        if hasattr(summary_obj, "text"):
                            reasoning_texts.append(str(summary_obj.text))
                        elif isinstance(summary_obj, dict) and "text" in summary_obj:
                            reasoning_texts.append(str(summary_obj["text"]))
            # Extract main output text from content
            content_list = getattr(item, "content", [])
            if isinstance(content_list, list):
                for content_item in content_list:
                    if hasattr(content_item, "text"):
                        main_texts.append(str(content_item.text))
                    elif isinstance(content_item, dict) and "text" in content_item:
                        main_texts.append(str(content_item["text"]))

    # Combine the output
    result = ""
    if main_texts:
        result += "\n".join(main_texts)
    if reasoning_texts:
        if result:
            result += "\n\n[Reasoning]\n"
        result += "\n".join(reasoning_texts)
    if not result:
        result = str(response)
    return result


def extract_claude_output(response):
    """
    Extracts both 'thinking' steps and the final output text from a Claude (Anthropic) response.

    The function searches the 'content' field of the response for items of type 'thinking'
    (collecting all such reasoning steps), and for the final output, usually of type 'text'.
    The output is concatenated: the final result text followed by all 'thinking' steps, 
    each separated by a newline. If no expected fields are found, falls back to stringifying the response.

    Args:
        response: The response object returned by the Claude/Anthropic API.

    Returns:
        str: A string containing the final result and, if present, the concatenated 'thinking' steps.
    """

    thinking_list = []
    result = None

    if hasattr(response, "content"):
        content = response.content
    elif isinstance(response, dict) and "content" in response:
        content = response["content"]
    else:
        content = None

    if isinstance(content, str):
        result = content
    elif isinstance(content, list) and len(content) > 0:
        for item in content:
            if (isinstance(item, dict) and item.get("type") == "thinking" and "thinking" in item):
                thinking_list.append(item["thinking"])
            elif hasattr(item, "type") and getattr(item, "type") == "thinking" and hasattr(item, "thinking"):
                thinking_list.append(item.thinking)
            if (isinstance(item, dict) and item.get("type") == "text" and "text" in item):
                result = item["text"]
            elif hasattr(item, "type") and getattr(item, "type") == "text" and hasattr(item, "text"):
                result = item.text
        if result is None and hasattr(content[0], "text"):
            result = content[0].text
        elif result is None and isinstance(content[0], dict) and "text" in content[0]:
            result = content[0]["text"]
        elif result is None:
            result = str(content[0])
    elif content is not None:
        result = str(content)
    else:
        result = str(response)

    final_output = str(result)
    if thinking_list:
        final_output += "\n".join(thinking_list) + "\n"

    return final_output

class LLMJudge:
    def __init__(
        self, 
        provider="openai",  # or "anthropic"
        model_name="o4-mini",
    ):
        """
        Initialize the LLMJudge.
        """
        self.openai_client = openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.claude_client = AnthropicBedrock(
            aws_access_key=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_region="us-east-1"
        )
        self.provider = provider
        self.model_name = model_name

    def judge_directory(
        self,
        image_directory: str,
        task_description: str,
        n_images: int = 5,   # number of images to use for judgment
        system_prompt: str = None,
        max_tokens: int = 20000,
        temperature: float = 0.0
    ):
        """
        Judge task completion given a directory of images and a task description.

        Args:
            image_directory: Directory containing PNG images (will be sorted).
            task_description: Task description string.
            n_images: Number of images to use (will even-sample if more exist).
            system_prompt: LLM system prompt.
            max_tokens: LLM output max tokens.
            temperature: LLM temperature.

        Returns:
            int: 1 if task completed, 0 otherwise.
            str: Raw LLM output.
        """

        print(f"inspecting images in: {image_directory}")
        files = [f for f in os.listdir(image_directory) if f.lower().endswith(".png")]
        files.sort()
        if not files:
            raise ValueError("No PNG images found in the directory.")
        total = len(files)
        chosen_indices = even_sample_indices(total, n_images)
        chosen_files = [os.path.join(image_directory, files[i]) for i in chosen_indices]
        return self.judge(
            image_paths=chosen_files,
            task_description=task_description,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

    def judge(
        self, 
        image_paths: List[str], 
        task_description: str,
        system_prompt: str = None,
        max_tokens: int = 20000,
        budget_tokens: int = 10000,
        temperature: float = 0.0
    ):
        """
        Judge task completion by sending images and task description to the LLM.

        Args:
            image_paths: List of PNG file paths (order matters: from start to finish).
            task_description: String describing the goal.
            system_prompt: Optional system prompt. Uses a default if not provided.
            max_tokens: Maximum LLM output tokens.
            temperature: LLM temperature.

        Returns:
            int: 1 if task is completed, 0 otherwise.
            str: Raw LLM output for reference/debugging.
        """
        if not image_paths:
            raise ValueError("No images provided for judgment.")
        
        # print(f"image paths: {image_paths}")

        if not system_prompt:
            system_prompt = """
Begin with **Yes** or **No**, followed by a brief statement explaining your judgment.
"""

        if self.provider == "openai":
            inputs = [
                {
                    "role": "developer",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": []
                }
            ]
            for img_path in image_paths:
                inputs[1]["content"].append({
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{png_to_base64(img_path)}",
                    "detail": "high"
                })
            inputs[1]["content"].append({
                "type": "input_text",
                "text": f"Task description: {task_description}"
            })

            response = self.openai_client.responses.create(
                model=self.model_name,
                reasoning={
                    "effort": "high",
                    "summary": "auto"
                },
                max_output_tokens=max_tokens,
                input=inputs
            )
            # print(response)
            result = extract_openai_output(response)

        elif self.provider == "anthropic":
            messages = []
            for img_path in image_paths:
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": png_to_base64(img_path),
                            },
                        },
                    ]
                })
            messages.append({
                "role": "user",
                "content": f"Task description: {task_description}"
            })
            response = self.claude_client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                system=system_prompt,
                thinking={
                    "type": "enabled",
                    "budget_tokens": budget_tokens
                },
                messages=messages
            )
            result = extract_claude_output(response)
        else:
            raise ValueError("provider must be 'openai' or 'anthropic'.")

        lower = result.lower()
        if lower.strip().startswith("yes"):
            return 1, result
        elif lower.strip().startswith("no"):
            return 0, result
        return 0, result

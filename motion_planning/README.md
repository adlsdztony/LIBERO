# LIBERO Waypoint Collection

## 0. Before Use: Update your code 

In line 237-238 of `[conda folder]/envs/[libero env]/lib/python3.9/site-packages/robosuite/utils/input_utils.py`

Comment out the gains tunninig condition for `Keyboard` class under OSC_POSE control

```python
        drotation = drotation * 1.5 # if isinstance(device, Keyboard) else drotation * 50
        dpos = dpos * 75 # if isinstance(device, Keyboard) else dpos * 125
```

**Quick Start:** Collect waypoints → Generate demonstrations

## 1. Collect Waypoints
```bash
python motion_planning/collect_waypoints.py
```

**Controls:**
- Move: `W/A/S/D/R/F`, Rotate: `Z/X/T/G/C/V`
- Gripper: `SPACEBAR` (toggle), Record: `J`, Quit: `Q`

**Key:** Press `J` at critical moments (before grasp, after grasp, at goal)

## 2. Generate Demonstrations
```bash
python motion_planning/auto_collect_demonstration.py
```

## Custom Tasks
```bash
python motion_planning/collect_waypoints.py --bddl-file "path/to/task.bddl"
python motion_planning/auto_collect_demonstration.py --bddl-file "path/to/task.bddl"
```

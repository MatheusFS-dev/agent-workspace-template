# Workflow: Debugging

Use this workflow for failures, crashes, environment issues, driver issues, CUDA problems, package conflicts, Python path errors, OS problems, dependency problems, and installation failures.

## 1. Core principle

Diagnose first. Fix second.

Do not ask the user to install, uninstall, upgrade, delete, edit files, change drivers, restart services, reboot, or modify persistent configuration before evidence has been collected.

## 2. First response requirements

Provide only read-only diagnostic commands.

For each command, explain:

- What it checks
- Why it matters
- Whether it is safe and read-only
- What output is important

Then provide one complete copy-paste diagnostic script.

## 3. Diagnostic command examples

Use only the commands that match the problem.

```bash
uname -a
lsb_release -a
python3 --version
python3 -c "import sys; print(sys.executable); print(sys.path)"
python3 -m pip --version
python3 -m pip list
nvidia-smi
nvcc --version
ldconfig -p | grep cuda || true
env | sort
```

Do not include fix commands in the diagnostic script.

## 4. After logs are provided

Analyze before fixing.

State:

- Confirmed facts
- Evidence
- Likely root cause
- Alternative causes
- Uncertainties
- Safest fix path

## 5. Fix response requirements

Only after diagnosis, provide fix commands.

For each fix command, explain:

- What it changes
- Why it is needed
- Risks
- How to revert when possible
- Success indicators
- Failure indicators

Then provide one complete copy-paste fix script.

## 6. Risk control

Ask before destructive or risky actions, including:

- Deleting files
- Removing packages
- Purging drivers
- Changing boot configuration
- Editing system configuration
- Rebooting remote machines
- Touching production credentials
- Overwriting experiment outputs

## 7. Completion format

```text
Confirmed facts:
- ...

Likely root cause:
- ...

Safest fix path:
- ...

Commands:
- diagnostics run: ...
- fixes run: ...

Remaining uncertainty:
- ...
```

---
name: caffe
description: Keep this Mac awake — prevent display sleep, system sleep, and disk sleep so long jobs (renders, browser automation, downloads, training) run uninterrupted. Trigger when the user types "caffe", "caffe mode", "caffeinate", "keep awake", "no sleep", "อย่าให้เครื่องหลับ", "อย่าให้จอดับ", "กันเครื่องหลับ", "เปิดโหมดไม่หลับ", or "รันไปเรื่อยๆ". Also handles turning it off ("caffe off", "caffe stop", "ปิด caffe") and checking status ("caffe status").
---

# caffe — keep the Mac awake (macOS `caffeinate`)

A tiny utility skill. It manages a detached `caffeinate -dimsu` process so the machine
never sleeps while long-running work is in progress.

`-d` no display sleep · `-i` no idle sleep · `-m` no disk sleep · `-s` no system sleep · `-u` user-active.
The process is started with `nohup ... &` so it **survives closing this terminal / Claude Code session**
(but NOT a reboot — for a permanent setting use `sudo pmset`, offer it only if asked).

## macOS only — check before doing anything
`caffeinate` exists only on macOS. If this isn't macOS, stop and say so — don't run a command that
isn't there. Point the user at the equivalent (Linux: `systemd-inhibit` or the `caffeine` app;
Windows: `powercfg` / PowerToys Awake).

```bash
[ "$(uname)" = "Darwin" ] && command -v caffeinate >/dev/null \
  || { echo "caffe is macOS-only (got $(uname)) — not running"; exit 0; }
```

## Decide the intent from the user's words
- "caffe", "caffe mode", "keep awake", "เปิดโหมดไม่หลับ" → **ON**
- "caffe off", "caffe stop", "ปิด caffe", "ให้เครื่องหลับได้" → **OFF**
- "caffe status", "เช็ค caffe" → **STATUS**

Default to **ON** if ambiguous.

## ON — enable keep-awake
1. Check if already active so you don't stack duplicates:
   ```bash
   pgrep -f "caffeinate -dimsu" >/dev/null && echo "already on" || echo "not running"
   ```
2. If not running, start it **detached** (do NOT use the Bash tool's run_in_background — that ties
   it to the Claude session; `nohup` survives the terminal closing):
   ```bash
   nohup caffeinate -dimsu >/dev/null 2>&1 &
   ```
3. Verify and report the active assertions:
   ```bash
   sleep 1; pmset -g assertions | grep -E "PreventUserIdleDisplaySleep|PreventUserIdleSystemSleep|PreventSystemSleep"
   ```
4. Tell the user it's ON, that it survives closing the terminal but not a reboot, and how to turn it off
   (`caffe off`). Mention the clamshell caveat only if relevant: closing the laptop lid with no external
   display/power will still sleep.

## OFF — let the Mac sleep normally again
```bash
pkill -f "caffeinate -dimsu" && echo "caffe off" || echo "was not running"
```
Confirm it's off. Leave any system `caffeinate -i -t <n>` processes (those are short-lived OS ones) alone —
only target the `-dimsu` instance this skill starts.

## STATUS — report current state
```bash
pgrep -lf "caffeinate -dimsu" || echo "caffe is OFF"
pmset -g assertions | grep -E "PreventUserIdleDisplaySleep|PreventUserIdleSystemSleep"
```

## Notes
- macOS only. `setsid` is unavailable on macOS — use `nohup ... &`.
- Permanent (survives reboot) = `sudo pmset -a displaysleep 0 sleep 0 disksleep 0`. Only do this if the
  user explicitly asks; record the old values first (`pmset -g`) so it can be reverted.

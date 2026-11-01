# desktop-scripts

Small desktop helpers. Symlinked into `~/.local/bin`.

- `firefox-webapp` - creates a Firefox (firefox-frosted) web app with its own profile,
  launcher and frosted COSMIC look. Run without arguments for usage.
- `xonar-knob.py` - routes the ASUS Xonar U5 volume knob to the Xonar's digital sink only.
  Install the user service: `cp systemd/xonar-knob.service ~/.config/systemd/user/ && systemctl --user enable --now xonar-knob`

## AI-generated

This project is vibecoded: all of the code, patches and docs were written by
[Claude Code](https://claude.com/claude-code) using **Claude Opus 5.5**
(`claude-opus-5-5`) at **medium effort**. A human gave the directions and did
the testing, but did not review the code line by line.

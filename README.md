# desktop-scripts

Small desktop helpers. Symlinked into `~/.local/bin`.

- `firefox-webapp` - creates a Firefox (firefox-frosted) web app with its own profile,
  launcher and frosted COSMIC look. Run without arguments for usage.
- `xonar-knob.py` - routes the ASUS Xonar U5 volume knob to the Xonar's digital sink only.
  Install the user service: `cp systemd/xonar-knob.service ~/.config/systemd/user/ && systemctl --user enable --now xonar-knob`

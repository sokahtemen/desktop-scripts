# desktop-scripts

Small desktop helpers.

- `firefox-webapp` - creates a Firefox (firefox-frosted) web app with its own profile,
  launcher and frosted COSMIC look. Run without arguments for usage.
- `cosmic-firefox-sync` - copies COSMIC's frosted-glass colors (the "Glass opacity" setting)
  into the firefox-frosted `userChrome.css` tokens; restart Firefox afterwards. To run it
  whenever the theme changes: `systemctl --user enable --now "$PWD"/systemd/cosmic-firefox-sync.{service,path}`
- `xonar-knob.py` - routes the ASUS Xonar U5 volume knob to the Xonar's digital sink only.
  Install the user service: `systemctl --user enable --now "$PWD"/systemd/xonar-knob.service`

Install the scripts with `ln -s "$PWD"/<script> ~/.local/bin/`. The systemd commands
above link the units from this folder too, so edits here apply after
`systemctl --user daemon-reload`.

## AI-generated

This project is vibecoded: all of the code, patches and docs were written by
[Claude Code](https://claude.com/claude-code) using **Claude Opus 5.5**
(`claude-opus-5-5`) at **medium effort**, with a cleanup pass at **max effort**. A human gave the directions and did
the testing, but did not review the code line by line.

## License

MIT, see [LICENSE](LICENSE).

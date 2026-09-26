name: Update CS GO server stats
on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:
permissions:
  contents: write
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: true
      - name: Retrieve server statistics
        run: python3 scripts/update_servers.py
      - name: Commit updated statistics
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add data/server1.json data/server2.json
          if ! git diff --cached --quiet; then
            git commit -m "Update server statistics"
            git push
          fi

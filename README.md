# Bowling Scorer — Selenium + Python Practice UI

A small Flask web app wrapping the bowling-game scorer, built specifically
to give you a real UI to practice Selenium against: a form, a submit
button, a results section, and validation error messages.

## What's in this project

```
.
├── app.py                      # Flask web app
├── bowling_game.py              # scoring library (validation + scoring logic)
├── templates/index.html         # the UI itself
├── pages/bowling_page.py        # Selenium Page Object
├── conftest.py                  # pytest fixtures (driver, base_url)
├── test_ui_selenium.py          # the Selenium test suite
├── requirements.txt
└── .github/workflows/selenium-tests.yml   # runs the suite in CI
```

## The UI

Ten text inputs (`frame-0` through `frame-9`), each accepting comma-separated
rolls (e.g. `8,/` for a spare, `X` for a strike, `9,0` for an open frame).
A "Calculate Score" button submits the form. On success, the page shows the
cumulative score per frame (`score-0` .. `score-9`) and the final total
(`final-score`). On invalid input, an error message (`error-message`) is
shown instead — the element IDs are deliberately simple so they're easy
Selenium locators to practice with.

---

## Running it locally (Windows 11, virtual environment)

**1. Create and activate a virtual environment:**
```powershell
cd path\to\bowling_selenium_practice
python -m venv venv
venv\Scripts\Activate.ps1
```

**2. Install dependencies:**
```powershell
pip install -r requirements.txt
```

**3. Start the Flask app** (leave this terminal running):
```powershell
python app.py
```
You should see `Running on http://127.0.0.1:5000`. Open that URL in a
browser to confirm the form loads.

**4. In a second terminal** (activate the same venv again with
`venv\Scripts\Activate.ps1`), run the Selenium tests:
```powershell
pytest test_ui_selenium.py -v
```

By default the tests run **headless** (no visible browser window) so they're
fast and CI-friendly. To actually *watch* the browser click through the form
— genuinely useful the first few times, so you can see what Selenium is doing
— disable headless mode for that run:
```powershell
$env:HEADLESS = "false"
pytest test_ui_selenium.py -v
$env:HEADLESS = "true"   # reset afterward
```

You need Google Chrome installed for this. Selenium 4.6+ (already pinned in
`requirements.txt`) includes **Selenium Manager**, which automatically
downloads the matching chromedriver binary — no manual driver setup needed.

---

## Running it "online" — GitHub Actions (CI)

This is the standard way to prove your Selenium suite passes without anyone
needing to run it locally — the included workflow
(`.github/workflows/selenium-tests.yml`) does the following automatically
on every push:

1. Checks out the code and sets up Python
2. Installs dependencies from `requirements.txt`
3. Installs Chrome on the CI runner (`browser-actions/setup-chrome`)
4. Starts the Flask app in the background and waits until it responds
5. Runs the Selenium suite headlessly against `http://localhost:5000`
6. Prints the Flask app's logs if anything fails, to make debugging easy

**To use it, push this project to GitHub.** Full step-by-step below, with
both a browser-only path and a git-command path — pick whichever you're
more comfortable with.

### Step 1: Create the GitHub repo

1. Go to **https://github.com** and log in.
2. Click the **+** icon (top-right) → **New repository**.
3. Fill in:
   - **Repository name**: `bowling-selenium-practice` (or anything descriptive)
   - **Description** (optional): "Selenium + Python UI testing practice for the bowling scorer"
   - **Public or Private**: Public is simplest if you want to share the
     link; Private works too if you add collaborators later
   - **Do NOT check** "Add a README file" — you already have one, and it
     will conflict with the one in this project
4. Click **Create repository**.

### Step 2 (Path A): Browser-only — no git installed, easiest

1. On your new empty repo page, click **"uploading an existing file"**
   (the blue link in the middle of the page).
2. Drag in **every file and folder** from this project, keeping the
   folder structure intact:
   - `app.py`
   - `bowling_game.py`
   - `conftest.py`
   - `requirements.txt`
   - `README.md`
   - `templates/index.html`
   - `pages/bowling_page.py` and `pages/__init__.py`
   - `test_ui_selenium.py`
   - `.github/workflows/selenium-tests.yml`

   The GitHub upload page supports dragging entire folders in most
   browsers, and it will preserve the folder paths (`templates/`,
   `pages/`, `.github/workflows/`) automatically. If your browser only
   lets you pick individual files, drag one folder at a time.

   **Important:** the `.github` folder starts with a dot, so it's a
   hidden folder on Mac/Windows file explorers by default. Make sure your
   file explorer is set to show hidden files/folders before dragging, or
   the GitHub Actions workflow won't be included.

3. Scroll down to **"Commit changes"**, type a message like
   `Initial commit — Selenium practice project`, and click **Commit
   changes**.
4. Refresh the repo page and confirm you see all the files and folders
   listed, including a `.github` folder.

### Step 2 (Path B): Using git from your terminal

**One-time setup** (skip if git is already installed and configured):
```powershell
git --version
```
If that errors, install git (e.g. from git-scm.com on Windows), then:
```powershell
git config --global user.name "Bill Kwok"
git config --global user.email "bill_kwok@hotmail.com"
```

**Push the project:**
1. Open a terminal in this project's folder (the one containing `app.py`,
   `bowling_game.py`, `templates/`, `pages/`, etc.):
```powershell
cd path\to\bowling_selenium_practice
```
2. Initialize and commit:
```powershell
git init
git add .
git commit -m "Initial commit — Selenium practice project"
```
3. Confirm the `.github` folder was picked up (git tracks dotfiles/folders
   by default, so this should just work):
```powershell
git status
```
   You should see `.github/workflows/selenium-tests.yml` listed as tracked.
4. Back on GitHub, your empty repo page shows a URL like
   `https://github.com/YOUR-USERNAME/bowling-selenium-practice.git`. Copy it.
5. Connect and push:
```powershell
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/bowling-selenium-practice.git
git push -u origin main
```
6. If prompted for credentials: use a **Personal Access Token**, not your
   GitHub password (GitHub no longer accepts passwords for this). Generate
   one at GitHub → Settings → Developer settings → Personal access tokens
   → Tokens (classic) → Generate new token, check the `repo` scope, and
   paste it in place of your password when prompted (username stays as
   your GitHub username).

### Step 3: Verify the files landed correctly

Visit `https://github.com/YOUR-USERNAME/bowling-selenium-practice` and confirm:
- `app.py`, `bowling_game.py`, `conftest.py`, `requirements.txt`, `README.md` are all present at the top level
- `templates/index.html` exists
- `pages/bowling_page.py` exists
- `.github/workflows/selenium-tests.yml` exists — click into it to confirm the YAML content is there, not empty

### Step 4: Watch the workflow run

1. Click the **Actions** tab near the top of the repo page.
2. You should see a workflow run automatically kicked off, named
   **"Selenium UI Tests"** — GitHub Actions triggers on every push
   automatically, so you don't need to do anything extra to start it.
3. Click into the run. You'll see each step from `selenium-tests.yml`
   listed in order — checkout, Python setup, dependency install, Chrome
   setup, starting the Flask app, and running the Selenium tests.
4. Within a minute or two, it'll show a green checkmark ✅ if all 9 tests
   passed against a real headless Chrome instance, or a red ❌ with logs
   if something failed. Click into the "Run Selenium tests" step to see
   the full pytest output either way.

### Step 5 (optional polish): Add a status badge to your README

1. On the **Actions** tab, click into the "Selenium UI Tests" workflow in
   the left sidebar.
2. Click the **"..."** menu (top right) → **Create status badge** → copy
   the Markdown snippet.
3. Paste it at the top of `README.md`, commit, and push (either path
   above works for this small follow-up change).

### Common snags to watch for

- **Workflow doesn't appear in the Actions tab at all:** almost always
  means the `.github/workflows/selenium-tests.yml` file didn't actually
  get uploaded — usually because it was hidden and skipped during a
  drag-and-drop. Go back and check the repo's file list for the `.github`
  folder specifically.
- **"Set up Chrome" step fails:** rare, but if it happens, re-run the
  workflow (Actions tab → the failed run → "Re-run all jobs") — these
  community actions occasionally have transient hiccups.
- **Tests fail with a connection error to `localhost:5000`:** means the
  Flask app didn't start in time. Check the "Start Flask app in the
  background" step's log output for errors, and check the
  "Show Flask logs on failure" step at the bottom of the run — it prints
  `flask.log` automatically whenever a step fails.

---

## Optional: testing against a truly public URL

If you want to practice pointing Selenium at an app that's actually
deployed and publicly reachable (rather than `localhost` inside the same
CI job), you have two lightweight options:

**Option A — quick and temporary (ngrok):**
1. Run `python app.py` locally as normal.
2. In a separate terminal, run `ngrok http 5000` (after installing ngrok
   and signing up for a free account at ngrok.com).
3. ngrok gives you a public URL like `https://abcd1234.ngrok-free.app`.
4. Point your tests at it: `$env:BASE_URL = "https://abcd1234.ngrok-free.app"`
   before running `pytest test_ui_selenium.py -v`.
   This is great for a quick demo but the URL disappears when you stop ngrok.

**Option B — a real (free-tier) deployment (Render):**
1. Create a free account at render.com, connect your GitHub repo.
2. Create a new "Web Service," point it at this repo, with start command
   `python app.py` (or `gunicorn app:app` for a more production-appropriate
   setup — you'd add `gunicorn` to `requirements.txt` if so).
3. Render gives you a permanent public URL.
4. Set `BASE_URL` to that URL (locally, or as a GitHub Actions secret) and
   run the same test suite against it.

Neither of these is required to satisfy the technical assessment — the
local + GitHub Actions setup above is already a complete, realistic
Selenium + Python + CI workflow. These are just good "next step" options
if you want extra practice testing against something genuinely public.

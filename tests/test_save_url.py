import pytest
from unittest.mock import patch, MagicMock
from save_url import core, poethepoet, __version__, __versiondate__
import os

def test_humanizeFileSize():
    assert core.humanizeFileSize(500) == "500.00 B"
    assert core.humanizeFileSize(1024) == "1.00 KB"
    assert core.humanizeFileSize(1024 * 1024) == "1.00 MB"
    assert core.humanizeFileSize(1024 * 1024 * 1024) == "1.00 GB"

def test_search_backend_success():
    with patch("save_url.core.which", return_value="/usr/bin/single-file"):
        path = core.search_backend("singlefile")
        assert path == "/usr/bin/single-file"

    with patch("save_url.core.which", return_value="/usr/bin/monolith"):
        path = core.search_backend("monolith")
        assert path == "/usr/bin/monolith"

def test_search_backend_invalid():
    with pytest.raises(SystemExit) as exc_info:
        core.search_backend("unknown_backend")
    assert exc_info.value.code == 2

def test_search_backend_missing():
    with patch("save_url.core.which", return_value=None):
        with pytest.raises(SystemExit) as exc_info:
            core.search_backend("singlefile")
        assert exc_info.value.code == 2

def test_normalize_url():
    assert core.normalize_url("www.kde.org") == "https://www.kde.org"
    assert core.normalize_url("https://www.kde.org") == "https://www.kde.org"
    assert core.normalize_url("http://example.com") == "http://example.com"

def test_find_binary():
    with patch("save_url.core.which", side_effect=lambda b: "/usr/bin/chromium" if b == "chromium" else None):
        assert core.find_binary("chromium") == "/usr/bin/chromium"
        assert core.find_binary(["nonexistent", "chromium"]) == "/usr/bin/chromium"

    with patch("save_url.core.which", return_value=None):
        assert core.find_binary(["nonexistent1", "nonexistent2"]) is None

def test_run_backend_with_browser():
    mock_result = MagicMock()
    mock_result.stdout = b"<html><head><title>Test</title></head><body>Hello</body></html>"
    mock_result.returncode = 0

    with patch("save_url.core.search_backend", return_value="/usr/bin/single-file"), \
         patch("save_url.core.find_binary", side_effect=lambda names: "/usr/bin/chromium" if "chromium" in names else "/usr/bin/single-file"), \
         patch("save_url.core.run", return_value=mock_result) as mock_run:
        content, code = core.run_backend("https://example.com", "singlefile")
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert cmd[0] == "/usr/bin/single-file"
        assert "--browser-executable-path=/usr/bin/chromium" in cmd
        assert any(arg.startswith("--browser-script=") for arg in cmd)
        assert any(arg.startswith("--browser-stylesheet=") for arg in cmd)
        assert "--dump-content" in cmd
        assert "https://example.com" in cmd

def test_run_backend_monolith():
    mock_result = MagicMock()
    mock_result.stdout = b"<html><head><title>Test</title></head><body>Hello</body></html>"
    mock_result.returncode = 0

    with patch("save_url.core.search_backend", return_value="/usr/bin/monolith"), \
         patch("save_url.core.run", return_value=mock_result) as mock_run:
        content, code = core.run_backend("https://example.com", "monolith")
        assert "Hello" in content
        assert code == 0
        mock_run.assert_called_once_with(["/usr/bin/monolith", "https://example.com"], shell=False, stdout=core.PIPE)

def test_run_backend_fallback_to_monolith():
    mock_result = MagicMock()
    mock_result.stdout = b"<html><head><title>Test</title></head><body>Hello</body></html>"
    mock_result.returncode = 0

    with patch("save_url.core.find_binary", side_effect=lambda names: "/usr/bin/monolith" if "monolith" in names else None), \
         patch("save_url.core.search_backend", return_value="/usr/bin/monolith"), \
         patch("save_url.core.run", return_value=mock_result) as mock_run:
        content, code = core.run_backend("https://example.com", "singlefile")
        assert "Hello" in content
        assert code == 0
        mock_run.assert_called_once_with(["/usr/bin/monolith", "https://example.com"], shell=False, stdout=core.PIPE)

def test_run_backend_no_browser_no_monolith():
    with patch("save_url.core.find_binary", return_value=None):
        with pytest.raises(SystemExit) as exc_info:
            core.run_backend("https://example.com", "singlefile")
        assert exc_info.value.code == 2

def test_getTitle_from_content():
    html = "<html><head><title>Direct Title</title></head></html>"
    title = core.getTitle("https://example.com", html)
    assert title == "Direct Title"

def test_getTitle_mechanize():
    mock_browser = MagicMock()
    mock_browser.title.return_value = "Example Title\n/ "
    with patch("save_url.core.Browser", return_value=mock_browser):
        title = core.getTitle("https://example.com", "")
        assert title == "Example Title"

def test_getTitle_none():
    with patch("save_url.core.Browser", side_effect=Exception("Browser failed")):
        title = core.getTitle("https://example.com", "<html><head></head></html>")
        assert title is None

def test_input_string():
    with patch("builtins.input", side_effect=["", "My Custom Title"]):
        val = core.input_string("Write title")
        assert val == "My Custom Title"

def test_save_url_flow(tmp_path):
    os.chdir(tmp_path)
    mock_html = "<html><head><title>Test Page</title></head><body>Content</body></html>"
    with patch("save_url.core.run_backend", return_value=(mock_html, 0)), \
         patch("save_url.core.getTitle", return_value="Test Page"):
        core.save_url("https://example.com", notime=False, backend="singlefile")
        files = list(tmp_path.glob("*.html"))
        assert len(files) == 1
        assert "Test Page.html" in files[0].name
        with open(files[0], "r", encoding="utf-8") as f:
            assert f.read() == mock_html

def test_save_url_notime(tmp_path):
    os.chdir(tmp_path)
    mock_html = "<html><head><title>Test Page</title></head><body>Content</body></html>"
    with patch("save_url.core.run_backend", return_value=(mock_html, 0)), \
         patch("save_url.core.getTitle", return_value="Test Page"):
        core.save_url("https://example.com", notime=True, backend="singlefile")
        expected_file = tmp_path / "Test Page.html"
        assert expected_file.exists()
        with open(expected_file, "r", encoding="utf-8") as f:
            assert f.read() == mock_html

def test_save_url_prompt_title_when_none(tmp_path):
    os.chdir(tmp_path)
    mock_html = "<html><body>No Title</body></html>"
    with patch("save_url.core.run_backend", return_value=(mock_html, 0)), \
         patch("save_url.core.getTitle", return_value=None), \
         patch("save_url.core.input_string", return_value="Prompted Title"):
        core.save_url("https://example.com", notime=True, backend="singlefile")
        expected_file = tmp_path / "Prompted Title.html"
        assert expected_file.exists()

def test_save_url_error_content(tmp_path):
    os.chdir(tmp_path)
    with patch("save_url.core.run_backend", return_value=("", 1)), \
         patch("save_url.core.getTitle", return_value="Error Page"), \
         patch("save_url.core.colors.red") as mock_red:
        core.save_url("https://example.com", notime=True, backend="singlefile")
        mock_red.assert_called()

def test_console_save_url_args():
    with patch("sys.argv", ["save_url", "https://example.com", "--notime", "-b", "monolith"]), \
         patch("save_url.core.save_url") as mock_save:
        core.console_save_url()
        mock_save.assert_called_once_with("https://example.com", True, "monolith")

def test_poethepoet_tasks(capsys):
    poethepoet.release()
    out = capsys.readouterr().out
    assert "Nueva versión:" in out

    poethepoet.monolith_ebuild()
    out2 = capsys.readouterr().out
    assert "Procedure to update monolith ebuild" in out2

    with patch("save_url.poethepoet.system") as mock_sys, \
         patch("save_url.poethepoet.makedirs") as mock_dirs:
        poethepoet.translate()
        assert mock_sys.called
        poethepoet.pytest()
        assert mock_sys.called

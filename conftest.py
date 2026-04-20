import pytest
from playwright.sync_api import sync_playwright

# 📸 capture test result status
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def page(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)

        context = browser.new_context()

        # 🔍 start trace
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = context.new_page()
        yield page

        # 📌 if test failed → save screenshot + trace
        if request.node.rep_call.failed:
            page.screenshot(
                path=f"test-results/screenshots/{request.node.name}.png",
                full_page=True
            )

            context.tracing.stop(
                path=f"test-results/traces/{request.node.name}.zip"
            )
        else:
            context.tracing.stop()

        context.close()
        browser.close()
from playwright.sync_api import sync_playwright
import time
import datetime
import os, sys


def main():
    with sync_playwright() as p:
        # create a persistent browser
        browser = p.chromium.launch_persistent_context("browser_data", headless=False)
        page = browser.new_page()
        page.goto("https://otter.ai/signin")
        #id=otter-email-input
        # wait for user input, and when they press enter, continue
        input("Please login to your otter account, and then press enter to continue...")
        while True:
            try:
                try:page.goto("https://otter.ai/my-notes")
                except:
                    # try again
                    time.sleep(20)
                    continue
                time.sleep(10)
                # find class="conversation-list-item --selectable --has-menu --touch-enabled"
                try:a = page.query_selector(".conversation-list-item")
                except:
                    print("All notes have been exported")
                    page.close()
                    browser.close()
                    exit()
                a_tag = a.query_selector("a")
                # go to the link
                link = "https://otter.ai" + a_tag.get_attribute("href")
                page.goto(link)
                time.sleep(10)
                # find id=conversation-header-relative-time
                title = page.query_selector("#conversation-header-relative-time").inner_text()
                extra = title.split(", ")[0] +", "
                # replace extra with ""
                title = title.replace(extra, "")
                date = title.split(" .")[0]
                # convert date Sep 11, 2023 to 11-09-2023
                date = datetime.datetime.strptime(date, "%b %d, %Y").strftime("%m-%d-%Y")
                title = date+ " " + title.split(" . ")[1]
                # click on aria-label="Edit Note"
                page.click('[aria-label="Edit Note"]')
                # press ctrl+v
                time.sleep(1)
                # enter the title in class="otter-editor__content-editor --multi-row"
                page.fill(".otter-editor__content-editor", title)
                time.sleep(1)
                # click on class="mat-tooltip-trigger head-bar__menu-button"
                page.click(".mat-tooltip-trigger.head-bar__menu-button")
                time.sleep(1)
                # find div class local-options-menu
                div = page.query_selector(".local-options-menu")
                # in that, get all li tags
                export = div.query_selector_all("li")[2]
                # click on that
                export.click()
                time.sleep(2)
                # click on id="export-panel-button-cancel"
                with page.expect_download() as download_info:
                    page.click("#export-panel-button-complete")
                    download = download_info.value
                    download.save_as(download.suggested_filename)
                time.sleep(5)
                page.click(".mat-tooltip-trigger.head-bar__menu-button")
                # find div class local-options-menu
                div = page.query_selector(".local-options-menu")
                # in that, get all li tags
                delete = div.query_selector_all("li")[-1]
                # click on that
                delete.click()
                time.sleep(1)
                #click on single-confirm-overlay-primary-action
                page.click("#single-confirm-overlay-primary-action")
                time.sleep(5)
            except KeyboardInterrupt:
                print("Program stopped by user")
                page.close()
                browser.close()
                # exit the program
                exit()
            except Exception as e:
                print(e)
                print("Error occured, restarting...")
                # close page and browser and auto restart
                continue
if __name__ == "__main__":
    while True:
        main()

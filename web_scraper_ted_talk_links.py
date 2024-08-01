import asyncio
from playwright.async_api import async_playwright

async def click_with_retry(page, selector, max_attempts=5, delay=0.5):
    for attempt in range(max_attempts):
        try:
            element = await page.wait_for_selector(selector, timeout=5000)  # 5 seconds timeout
            await element.wait_for_element_state('visible')
            await element.wait_for_element_state('enabled')
            await element.click()
            print(f"Clicked element with selector: {selector}")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for selector {selector}: {e}")
            await asyncio.sleep(delay)
    print(f"Failed to click element with selector: {selector} after {max_attempts} attempts")
    return False

async def select_option_with_retry(page, selector, option_value, max_attempts=5, delay=0.5):
    for attempt in range(max_attempts):
        try:
            dropdown = await page.wait_for_selector(selector, timeout=5000)  # 5 seconds timeout
            await dropdown.select_option(value=option_value)
            print(f"Selected option '{option_value}' in dropdown with selector: {selector}")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for selector {selector} and option {option_value}: {e}")
            await asyncio.sleep(delay)
    print(f"Failed to select option '{option_value}' in dropdown with selector: {selector} after {max_attempts} attempts")
    return False

async def select_cantonese_subtitle(page):
    try:
        # Wait for the language dropdown to be available
        await page.wait_for_selector("select[data-testid='transcript__language-dropdown']", timeout=10000)
        # Select the Cantonese option (assuming "zh" is the value for Cantonese)
        await select_option_with_retry(page, "select[data-testid='transcript__language-dropdown']", "zh")
        print("Cantonese subtitles selected.")
    except Exception as e:
        print(f"Error selecting Cantonese subtitles: {e}")

async def scrape_cantonese_subtitles(url):
    async with async_playwright() as p:
        try:
            print("Launching the browser...")
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            print(f"Navigating to {url}...")
            await page.goto(url, timeout=120000)
            print("Successfully navigated to TED Talks.")

            # Handle the privacy preference center
            try:
                print("Handling privacy preference center...")
                await click_with_retry(page, "button:has-text('Reject All')")
            except Exception as e:
                print("Privacy preference center not found or already handled.")

            print("Waiting for the page to load completely...")
            await page.wait_for_load_state('networkidle', timeout=60000)
            print("Page loaded.")

            # Select Cantonese subtitles
            await select_cantonese_subtitle(page)

            # Wait for the transcript container to be available
            await page.wait_for_selector("div[data-testid='paragraphs-container']", timeout=10000)

            # Scrape the transcript
            transcript_elements = await page.query_selector_all("div[data-testid='paragraphs-container'] div[role='button'] span.text-textPrimary-onLight")

            print(f"Found {len(transcript_elements)} transcript elements.")
            if not transcript_elements:
                print(f"No transcript elements found for {url}")
            else:
                subtitles_text = []  # List to store scraped subtitles
                for element in transcript_elements:
                    text = await element.inner_text()  # Get the inner text of each span
                    subtitles_text.append(text.strip())  # Append the text to the list, stripping any extra whitespace
                    print(f"Scraped text: {text.strip()}")  # Print the scraped text

            await browser.close()  # Close the browser
            return subtitles_text  # Return the scraped subtitles
        except Exception as e:
            print(f"Error in scrape_cantonese_subtitles: {e}")

async def main():
    url = 'https://www.ted.com/talks'
    try:
        subtitles = await scrape_cantonese_subtitles(url)
        if subtitles:
            with open('cantonese_subtitles.txt', 'w', encoding='utf-8') as file:  # Ensure UTF-8 encoding
                for subtitle in subtitles:
                    file.write(subtitle + '\n')
            print("Subtitles successfully scraped and saved.")
        else:
            print("No subtitles were scraped.")
    except Exception as e:
        print(f"Error in main: {e}")

# Run the async main function
asyncio.run(main())
import subprocess
from scraper.content_parser import convert_pdf, convert_image
from typing import Union, List, Tuple
import json
import requests
import random
import string
import os


START_OF_MENU = "### START OF MENU ###\n"
END_OF_MENU = "### END OF MENU ###\n"


def _post_processing(output_file: str, convert_local: bool) -> Tuple[str, List[str]]:
    print("starting post processing")

    # store the content of everything
    content = ""

    # also store the links of images and pdf files
    links = []

    # load the json file
    with open(output_file, "r") as file:
        data = json.load(file)

    # check if the data contains a PDF link
    pdf_links = [item["menu_pdf"] for item in data if "menu_pdf" in item]
    for pdf_link in pdf_links:
        # download the PDF file
        pdf_url = pdf_link

        links.append(pdf_url)

        if not convert_local:
            continue

        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        pdf_file = f"menu_{random_string}.pdf"

        response = requests.get(pdf_url)
        with open(pdf_file, "wb") as f:
            f.write(response.content)

        # convert the PDF to text
        text = START_OF_MENU
        try:
            text = convert_pdf(pdf_file)
            print(f"converted pdf: {text}")
        except Exception as e:
            print(f"Error converting PDF: {e}")

        # store the text in the content
        text += END_OF_MENU
        content += text

        # delete the PDF file again
        subprocess.run(["rm", pdf_file])

    # check if the data contains an image link
    image_links = [item["menu_image"] for item in data if "menu_image" in item]
    for image_link in image_links:
        # download the image file
        image_url = image_link

        links.append(image_url)

        if not convert_local:
            continue

        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        image_file = f"menu_{random_string}.jpg"

        response = requests.get(image_url)
        with open(image_file, "wb") as f:
            f.write(response.content)

        # convert the image to text
        text = START_OF_MENU
        try:
            text = convert_image(image_file)
            print(f"converted image: {text}")
        except Exception as e:
            print(f"Error converting image: {e}")

        # store the text in the content
        text += END_OF_MENU
        content += text

        # delete the image file again
        subprocess.run(["rm", image_file])

    # check if the data contains text
    text = [item["menu_text"] for item in data if "menu_text" in item]
    for t in text:
        content += START_OF_MENU

        t += END_OF_MENU
        content += t

    return content, links


def scraper(
    url: str, convert_pdfs_local: bool = False
) -> Union[Tuple[str, List[str]], None]:
    """
    Executes the Scrapy spider to extract menu information 
    from a given URL and returns the parsed content.

    Args:
        url (str): The URL of the restaurant's website 
        from which the data is to be extracted.

    Returns:
        Union[Tuple[str, List[str]], None]: A tuple containing the scraped data as a string 
        and a list of links if successful, 
        or None if an error is encountered.
    """

    # Run the Scrapy spider with the given URL and save the output to the specified file
    try:
        output_file = os.path.join(os.getcwd(), "menu.json")
        process = subprocess.Popen(
            [
                "scrapy",
                "crawl",
                "menu_spider",
                "-a",
                f"start_url={url}",
                "-O",
                output_file,
            ],
            # TODO: this may need to be adjusted
            cwd="scraper",
        )
        process.wait()
        content, links = _post_processing(output_file, convert_pdfs_local)

        # delete the output file again
        subprocess.run(["rm", output_file])

        return content, links

    except Exception as e:
        print(f"Error running scraper: {e}")
        return None


# if __name__ == "__main__":
#     text = _post_processing("test.json")
#     print("Extracted text: ", text)

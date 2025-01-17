import re

from .type_definitions import Header


def generate_recommendations(tree) -> None:
    """Generate recommendations from a tree of Docx files.

    There is one file that contains a paragraph with contents:
    <!-- will compile recommendations from articles -->
    This function reads all articles and generates a list of recommendations, which are then written to the file.

    The file that needs to be replaced is one in section "Introduction",
    The files that need to be inserted are in section "Articles".
    All articles have a title (h1) and a recommendations section (first h2), and then more content.
    We are interested in the recommendations section. That's the one we will add to the recommendations file.
    """
    recommendation_elements = []
    recommendation_references = []

    for _, section in enumerate(tree):
        if section["text"] == "Chapters":
            for item in section["items"]:
                found_recommendations = False

                for i, element in enumerate(item.document.elements):
                    if isinstance(element, Header) and element.level == 2:
                        found_recommendations = True
                        start_index = i
                        h = Header(level=element.level, text=item.title)
                        recommendation_elements.append(h)
                        break

                if found_recommendations:
                    for element in item.document.elements[start_index + 1 :]:
                        if isinstance(element, Header) and element.level == 2:
                            break

                        if hasattr(element, "text") and element.text:
                            match = re.search(r"\[(.*?)\]", element.text)
                            if match:
                                ref_code = match.group(1)
                                # Try to find the reference in the document's references
                                found_ref = next(
                                    (ref for ref in item.document.references if ref.code.lower() == ref_code.lower()),
                                    None,
                                )
                                if found_ref:
                                    # If the reference is found, add it to the recommendation references
                                    recommendation_references.append(found_ref)

                        recommendation_elements.append(element)
                else:
                    print("Recommendations not found in", item.title)

    for _, section in enumerate(tree):
        if section["text"] == "Introduction":
            for item in section["items"]:
                if item.title == "Recommendations":
                    for ref in recommendation_references:
                        item.add_reference(ref)

                    for element in recommendation_elements:
                        item.add_element(element)

    return tree

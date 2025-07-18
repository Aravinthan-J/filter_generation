from langchain.agents import tool
import requests


@tool
def get_form_field_details(field_id: str) -> list[dict]:
    """
    Fetches metadata of a form field given its ID.

    This tool returns the name and standardized type of the field based on internal type mapping.
    It also determines if the field uses predefined list values (like dropdowns, users, or references).

    Args:
        field_id (str): The ID of the field to fetch metadata for.

    Returns:
        list[dict]: Metadata including field name, type, and whether it uses list values.
    """
    map = {'Text': 'String', 'Textarea': 'String', 'Email': 'Email', 'Number': 'Number', 'StarRating':
        'Number', 'Slider': 'Number', 'Date': 'Date', 'DateTime': 'DateTime', 'Currency': 'Currency', 'User': 'User',
           'UserAndGroup': 'UserAndGroup', 'MultiUser': 'UserList', 'Reference': 'Reference', 'Select': 'String',
           'Multiselect': 'StringList', 'Geolocation': 'Geolocation', 'JSON': 'JSON', 'Boolean': 'Boolean',
           'Attachment': 'JSONList', 'Image': 'JSON', 'Signature': 'JSON', 'Checklist': 'CheckList',
           'Checkbox': 'StringList', 'Aggregation': 'Aggregation', 'RemoteLookup': 'JSON', 'XML': 'XML',
           'SequenceNumber': 'String', 'SmartAttachment': 'JSONList', 'Radio': 'Select', 'Scanner': 'String',
           'Object': 'Object', 'ObjectList': 'ObjectList', 'StringList': 'StringList'}

    url = "https://localhost.tst.zingworks.com/case/2/Ac9iuLeMiQYd/Editable_grid/view/Normal_fields/fields"

    headers = {
        'x-access-key-id': 'Ak4633543b-63c3-4c46-b11d-2778a054e4e5',
        'x-access-key-secret': 'cEppav5y469Nb-j-o5IROK3n0iD-Dpm9-wnCGp7QdMMXzq-a8kxm3bZ9zafMNfKchKf1OV4z8SGYLGvi6vOQ'
    }

    response = requests.request("GET", url, headers=headers).json()
    form_field_map = {}
    for field in response:
        form_field_map[field["Id"]] = field

    if field_id not in form_field_map:
        return f"No such field with this field_id {field_id}"
    form_field_map[field_id]["is_use_list_values"] = True if form_field_map[field_id]["Type"] in [
        "Select",
        "Multiselect",
        "User",
        "MultiUser",
        "List",
        "Reference",
        "Groups",
        "DropdownList",
        "UserGroupList",
        "Roles"] or field_id in ("_status_name", "_priority_name", "_state_name", "_category") else False
    form_field_map[field_id]["Type"] = map.get(form_field_map[field_id]["Type"], "String")

    return form_field_map.get(field_id)


@tool
def get_form_field_attributes(field_id: str):
    """
    Returns sub-field attributes for special types like Currency or User fields.

    If the field is of a type with nested attributes (e.g. Currency has Unit & Value),
    this tool returns the attribute structure.

    Args:
        field_id (str): The ID of the field whose attributes need to be fetched.

    Returns:
        list[dict] | str: A list of attribute objects or a string if the field is not found or has no attributes.
    """
    map = {'Text': 'String', 'Textarea': 'String', 'Email': 'Email', 'Number': 'Number', 'StarRating':
        'Number', 'Slider': 'Number', 'Date': 'Date', 'DateTime': 'DateTime', 'Currency': 'Currency', 'User': 'User',
           'UserAndGroup': 'UserAndGroup', 'MultiUser': 'UserList', 'Reference': 'Reference', 'Select': 'String',
           'Multiselect': 'StringList', 'Geolocation': 'Geolocation', 'JSON': 'JSON', 'Boolean': 'Boolean',
           'Attachment': 'JSONList', 'Image': 'JSON', 'Signature': 'JSON', 'Checklist': 'CheckList',
           'Checkbox': 'StringList', 'Aggregation': 'Aggregation', 'RemoteLookup': 'JSON', 'XML': 'XML',
           'SequenceNumber': 'String', 'SmartAttachment': 'JSONList', 'Radio': 'Select', 'Scanner': 'String',
           'Object': 'Object', 'ObjectList': 'ObjectList', 'StringList': 'StringList'}

    url = "https://localhost.tst.zingworks.com/case/2/Ac9iuLeMiQYd/Editable_grid/view/Normal_fields/fields"

    headers = {
        'x-access-key-id': 'Ak4633543b-63c3-4c46-b11d-2778a054e4e5',
        'x-access-key-secret': 'cEppav5y469Nb-j-o5IROK3n0iD-Dpm9-wnCGp7QdMMXzq-a8kxm3bZ9zafMNfKchKf1OV4z8SGYLGvi6vOQ'
    }

    response = requests.request("GET", url, headers=headers).json()
    form_field_map = {}
    for field in response:
        form_field_map[field["Id"]] = field

    if field_id not in form_field_map:
        return "No such field with this field_id"
    form_field_map[field_id]["is_use_list_values"] = True if form_field_map[field_id]["Type"] in [
        "Select",
        "Multiselect",
        "User",
        "MultiUser",
        "List",
        "Reference",
        "Groups",
        "DropdownList",
        "UserGroupList",
        "Roles"] or field_id in ("_status_name", "_priority_name", "_state_name", "_category") else False

    if field_id not in form_field_map:
        return "No such field with this field_id"
    field = form_field_map[field_id]
    if field["Type"] in ["Currency"]:
        return [
            {
                "Id": "Unit",
                "Name": "Unit",
                "Type": "CurrencyUnit"
            },
            {
                "Id": "Value",
                "Name": "Value",
                "Type": "Number"
            }
        ]
    elif field["Type"] in ["User"]:
        return [
            {
                "Id": "Name",
                "Name": "Name",
                "Type": "Text"
            },
            {
                "Id": "Email",
                "Name": "Email address",
                "Type": "Text"
            },
            {
                "Id": "Manager",
                "Name": "Manager",
                "Type": "User"
            },
            {
                "Id": "Status",
                "Name": "Status",
                "Type": "Text"
            },
            {
                "Id": "Designation",
                "Name": "Job Title",
                "Type": "Text"
            }
        ]
    else:
        return field.get("Attributes") or f"No Attributes for this field_id {field_id}"


@tool
def get_form_field_values(field_id: str, page_number: int = 1, page_size: int = 50, search_string: str = "") -> dict:
    """
    Retrieves paginated and optionally filtered values for a form field that supports selectable options
    (e.g. dropdowns, user pickers, reference fields).

    This tool supports searching through the field values using a `search_string` parameter,
    which helps narrow down the results based on user input or partial matches.

    Args:
        field_id (str): ID of the form field to retrieve values for.
        page_number (int, optional): The page number to retrieve. Defaults to 1.
        page_size (int, optional): Number of items per page. Defaults to 50.
        search_string (str, optional): A search keyword to filter the values returned. If provided,
                                       the API performs a fuzzy match to return relevant entries.

    Returns:
        dict: A dictionary containing matching field values, pagination info, or an error message if the field is invalid.
    """
    try:
        url = f"https://localhost.tst.zingworks.com/case/2/Ac9iuLeMiQYd/Editable_grid/view/Normal_fields/field/{field_id}/values?q={search_string}&page_number={page_number}&page_size={page_size}"
        #url = f"https://localhost.tst.zingworks.com/case/2/Ac9iuLeMiQYd/Editable_grid/view/Normal_fields/field/{field_id}/values?q=viswa&page_number={page_number}&page_size={500}"

        headers = {
            'x-access-key-id': 'Ak4633543b-63c3-4c46-b11d-2778a054e4e5',
            'x-access-key-secret': 'cEppav5y469Nb-j-o5IROK3n0iD-Dpm9-wnCGp7QdMMXzq-a8kxm3bZ9zafMNfKchKf1OV4z8SGYLGvi6vOQ'
        }

        response = requests.request("GET", url, headers=headers).json()
    except Exception as ex:
        return f"No such field with this field_id {field_id}"
    return response


tools = [get_form_field_details, get_form_field_attributes, get_form_field_values]

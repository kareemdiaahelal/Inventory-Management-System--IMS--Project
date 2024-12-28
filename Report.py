import os
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{data_kind}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-8">
<div class="container text-center">
<h1 class="text-3xl font-bold mb-5" >Inventory Management System</h1>
</div>
    <div class="container mx-auto">
        <h1 class="text-2xl font-bold mb-2">{data_kind}</h1>
        <table class="table-auto w-full border-collapse border border-gray-300">
            {headers}
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

products_headers="""
<thead>
    <tr class="bg-gray-200">
        <th class="border border-gray-300 px-4 py-2">Name</th>
        <th class="border border-gray-300 px-4 py-2">Price</th>
        <th class="border border-gray-300 px-4 py-2">Quantity</th>
        <th class="border border-gray-300 px-4 py-2">ID</th>
        <th class="border border-gray-300 px-4 py-2">Created By</th>
    </tr>
</thead>
"""

def generate_table_rows_products(data):
    rows = ""
    for item in data:
        rows += f"""
        <tr >
            <td class='border border-gray-300 px-4 py-2'>{item['name']}</td>
            <td class='border border-gray-300 px-4 py-2'>{item['price']}</td>
            <td class='border border-gray-300 px-4 py-2'>{item['quantity']}</td>
            <td class='border border-gray-300 px-4 py-2'>{item['id']}</td>
            <td class='border border-gray-300 px-4 py-2'>{item['createdBy']}</td>
        </tr>
        """
    
    return rows

users_headers = """
<thead>
    <tr class="bg-gray-200">
        <th class="border border-gray-300 px-4 py-2">ID</th>
        <th class="border border-gray-300 px-4 py-2">Name</th>
        <th class="border border-gray-300 px-4 py-2">Email</th>
        <th class="border border-gray-300 px-4 py-2">Age</th>
        <th class="border border-gray-300 px-4 py-2">Role</th>
    </tr>
</thead>
"""

def generate_table_rows_users(data):
    rows = ""
    for item in data:
        rows += f"""
        <tr>
            <td class='border border-gray-300 px-4 py-2'>{item['id']}</td>
            <td class='border border-gray-300 px-4 py-2'>{item['name']}</td>
            <td class='border border-gray-300 px-4 py-2'>{item['email']}</td>
            <td class='border border-gray-300 px-4 py-2'>{item['age']}</td>
            <td class='border border-gray-300 px-4 py-2'>{item['role']}</td>
        </tr>
        """
    
    return rows

def create_report(data,file_name,model):
    try:
        if model=="users":
            headers=users_headers
            table_rows=generate_table_rows_users(data)
        else:
            headers=products_headers
            table_rows=generate_table_rows_products(data)
        html_content = html_template.format(rows=table_rows, data_kind=f"{model} data",headers=headers)

        with open(file_name, "w") as file:
            file.write(html_content)
        
        os.system(f"open {file_name}" if os.name == "posix" else f"start {file_name}")
        
    except Exception as e:
        print(f"An error occurred: {e}")


import os

LAST_RESULTS = []

def find_file(query: str, search_path="C:\\Users"):

    global LAST_RESULTS
    LAST_RESULTS = []

    query = query.lower()

    try:
        for root, dirs, files in os.walk(search_path):

            for file in files:

                if query in file.lower():

                    LAST_RESULTS.append(
                        os.path.join(root, file)
                    )

                    if len(LAST_RESULTS) >= 10:
                        break

            if len(LAST_RESULTS) >= 10:
                break

        return {
            "status": "success",
            "results": LAST_RESULTS
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


mocked_token = {
    "access": "access_token",
    "access_expires": 86400,
    "refresh": "refresh_token",
    "refresh_expires": 2592000,
}

def generate_mock(id):
    return {
        "count": 2,
        "results": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "created": "2022-02-21T15:41:40.350Z",
                "redirect": "https://nordigen.com",
            },
            {
                "id": id,
                "created": "2022-02-21T15:41:40.350Z",
                "redirect": "https://nordigen.com",
            },
        ]
    }

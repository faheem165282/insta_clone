from src import create_app
from flask import url_for

app = create_app()

with app.test_request_context():
    try:
        print("Testing consumer.gallery URL:")
        url = url_for('consumer.gallery')
        print(f"URL successfully generated: {url}")
    except Exception as e:
        print(f"Error generating URL: {e}")

    print("\nAll registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint} -> {rule.rule}")

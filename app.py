import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Configuration ---
DATA_FILE = 'fashion_data.json'
API_PREFIX = '/api' 

app = Flask(__name__)
CORS(app) 

# --- Data Loading ---

def load_data():
    """Loads product and FAQ data from the local JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return {"products": [], "faqs": [], "journal_entries": []}

SITE_DATA = load_data()


# --- Advanced Chatbot Logic ---

def get_bot_response(user_message):
    """
    Generates a response by searching products, FAQs, and using general knowledge.
    """
    message = user_message.lower()

    # 1. --- Search FAQ Data ---
    for faq in SITE_DATA.get('faqs', []):
        question = faq['question'].lower()
        # Look for keywords in the user message that match the FAQ question
        if any(keyword in message for keyword in question.split()):
            # Prioritize relevant keywords for common questions
            if ('return' in message or 'policy' in message) and 'return policy' in question:
                return f"Regarding returns: {faq['answer']}"
            if ('ship' in message or 'delivery' in message) and ('shipping' in question or 'delivery' in question):
                return f"For shipping: {faq['answer']}"
            if ('track' in message or 'order' in message) and 'track my order' in question:
                return f"For tracking: {faq['answer']}"
            if ('international' in message or 'worldwide' in message) and 'international shipping' in question:
                return f"For international shipping: {faq['answer']}"
            if ('payment' in message or 'accept' in message) and 'payment methods' in question:
                return f"Regarding payment: {faq['answer']}"


    # 2. --- Search Product Data ---
    product_keywords = ['product', 'item', 'coat', 'boots', 'scarf', 'hat', 'bag', 'jeans', 'new arrival']
    if any(keyword in message for keyword in product_keywords):
        
        # Try to find a specific product by name
        found_products = [
            p for p in SITE_DATA.get('products', []) 
            if p['name'].lower() in message or any(word in message for word in p['name'].lower().split())
        ]

        if found_products:
            # Return details for the first specific product found
            p = found_products[0]
            return (
                f"I found the **{p['name']}** in our collection! It's priced at **${p['price']:.2f}**. "
                f"Description: {p['description']}. It currently has a rating of {p['rating']} stars."
            )
        
        # If no specific product, list new arrivals (as featured on the main page)
        new_arrivals = [p['name'] for p in SITE_DATA.get('products', []) if p['_id'] in [1, 2, 3, 4]]
        if new_arrivals:
            new_arrivals_list = ', '.join(new_arrivals)
            return (
                f"We have many great fashion items! Our featured **New Arrivals** include: "
                f"**{new_arrivals_list}**. You can find them all on the products page! 🛍️"
            )


    # 3. --- Search Journal Data ---
    if 'journal' in message or 'style guide' in message or 'article' in message:
        latest_entry = SITE_DATA.get('journal_entries', [])[0] if SITE_DATA.get('journal_entries') else None
        if latest_entry:
            return (
                f"Our latest journal entry is **'{latest_entry['title']}'**. "
                f"It's about: {latest_entry['content'].strip('.')}. Check out the section below the New Arrivals! 📚"
            )


    # 4. --- General Chat and Fallback (Retaining original JS logic) ---
    if 'hello' in message or 'hi' in message or 'greetings' in message:
        return 'Hello! 👋 Welcome to Fashion-freek. How can I help you today?'
    elif 'price' in message or 'cost' in message:
        # Generic price response
        return 'Our prices vary by item, generally ranging from $45 to $180. Check the product page for exact costs! 💰'
    elif 'size' in message or 'fit' in message:
        return 'Please refer to our size guide on the product pages. Feel free to contact us for more details! 📏'
    elif 'contact' in message or 'support' in message or 'email' in message:
        return 'You can reach our support team at **support@fashion-freek.com** or call us at 1-800-FASHION. 📞'
    elif 'sale' in message or 'discount' in message or 'deal' in message:
        return 'We currently have exclusive deals! Subscribe to our newsletter to receive them directly in your inbox. 🎉'
    
    # Final Catch-all
    return 'Thanks for your message! I couldn\'t find a specific answer, but our team will get back to you soon. Is there anything else I can help you with?'


# --- Flask Routes ---

@app.route(f'{API_PREFIX}/chatbot', methods=['POST'])
def chatbot_endpoint():
    """Handles incoming POST requests from the chatbot frontend."""
    if not request.json or 'message' not in request.json:
        return jsonify({'status': 'error', 'message': 'Missing message data'}), 400

    user_message = request.json.get('message')
    bot_response = get_bot_response(user_message)
    
    return jsonify({
        'status': 'success',
        'message': bot_response
    })

@app.route('/')
def index():
    """A simple index route for testing if the server is running."""
    return "Fashion-freek Chatbot API is running! Access the endpoint at /api/chatbot"


# --- Server Execution ---

if __name__ == '__main__':
    print("Flask server running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
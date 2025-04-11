# app/generate.py

import os
import json
import openai
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from . import mongo

generate_bp = Blueprint('generate', __name__)

# 🔐 OpenRouter (OpenAI-compatible) setup
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENAI_API_KEY")


# ✅ Generate website content (JWT protected)
@generate_bp.route('/', methods=['POST'])
@jwt_required()
def generate_website_content():
    data = request.get_json()
    business_type = data.get('business_type', '').strip()
    industry = data.get('industry', '').strip()

    if not business_type or not industry:
        return jsonify({'error': 'Both business_type and industry are required'}), 400

    # Generate prompt
    prompt = f"""
You are a professional website content generator. Generate content for a website of a {business_type} in the {industry} industry.

Respond in the following JSON format:
{{
  "hero": {{
    "headline": "...",
    "subheadline": "..."
  }},
  "about": "...",
  "services": [
    {{ "title": "...", "description": "..." }},
    {{ "title": "...", "description": "..." }},
    {{ "title": "...", "description": "..." }}
  ],
  "contact": {{
    "email": "...",
    "phone": "...",
    "hours": "..."
  }}
}}

Only respond with valid JSON.
"""

    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )

        raw_content = response['choices'][0]['message']['content']
        try:
            website_data = json.loads(raw_content)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON returned by AI', 'raw': raw_content}), 500

        # Add user & timestamp
        website_data['user'] = get_jwt_identity()
        website_data['created_at'] = datetime.utcnow()

        result = mongo.db.websites.insert_one(website_data)
        website_id = str(result.inserted_id)

        return jsonify({
            'id': website_id,
            'message': 'Website content generated and saved',
            'content': website_data
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Preview generated site (JWT protected)
@generate_bp.route('/preview/<id>', methods=['GET'])
def preview_website(id):
    try:
        website = mongo.db.websites.find_one({"_id": ObjectId(id)})
        if not website:
            return "Website not found", 404

        return render_template(
            "preview.html",
            hero=website.get("hero", {}),
            about=website.get("about", ""),
            services=website.get("services", []),
            contact=website.get("contact", {})
        )

    except Exception as e:
        return f"Error: {str(e)}", 500


# ✅ List all websites (JWT protected)
@generate_bp.route('/list', methods=['GET'])
def list_websites():
    try:
        user = get_jwt_identity()
        websites = list(mongo.db.websites.find({'user': user}).sort('_id', -1))

        for site in websites:
            site['_id'] = str(site['_id'])

        return render_template("list.html", websites=websites)

    except Exception as e:
        return f"Error: {str(e)}", 500


# ✅ Delete website by ID (JWT protected)
@generate_bp.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete_website(id):
    try:
        user = get_jwt_identity()
        result = mongo.db.websites.delete_one({"_id": ObjectId(id), "user": user})

        if result.deleted_count == 0:
            return jsonify({'error': 'Website not found or unauthorized'}), 404

        return jsonify({'message': f'Website {id} deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Export preview as downloadable .html file
@generate_bp.route('/export/<id>.html', methods=['GET'])
@jwt_required()
def export_html(id):
    try:
        user = get_jwt_identity()
        website = mongo.db.websites.find_one({"_id": ObjectId(id), "user": user})
        if not website:
            return "Website not found", 404

        rendered = render_template(
            "preview.html",
            hero=website.get("hero", {}),
            about=website.get("about", ""),
            services=website.get("services", []),
            contact=website.get("contact", {})
        )

        response = make_response(rendered)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Disposition'] = f'attachment; filename=website_{id}.html'
        return response

    except Exception as e:
        return f"Error: {str(e)}", 500

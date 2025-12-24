from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_core.tools import tool, InjectedToolArg
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from typing import Annotated
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """
    This function fetches the currency conversion factor between a given base currency and a target currency
    """
    url = f'https://v6.exchangerate-api.com/v6/fb2068dde1a0f79e6fb18d10/pair/{base_currency}/{target_currency}'
    response = requests.get(url)
    return response.json()

@tool
def convert(base_currency_value: float, conversion_rate: Annotated[float, InjectedToolArg]) -> float:
    """
    Given a currency rate this function calculates the target currency value from a given base currency value
    """
    return base_currency_value * conversion_rate

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv('GROQ_API_KEY')
)
llm_with_tools = llm.bind_tools([get_conversion_factor, convert])

@app.route('/convert', methods=['POST'])
def convert_currency():
    try:
        data = request.json
        base_currency = data.get('base_currency', 'USD')
        target_currency = data.get('target_currency', 'PKR')
        amount = float(data.get('amount', 10))
        
        # Create message
        messages = [HumanMessage(
            f'What is the conversion factor between {base_currency} and {target_currency}, '
            f'and based on that can you convert {amount} {base_currency} to {target_currency}'
        )]
        
        # Get AI response
        ai_message = llm_with_tools.invoke(messages)
        messages.append(ai_message)
        
        conversion_rate = None
        converted_amount = None
        
        # Execute tools
        for tool_call in ai_message.tool_calls:
            if tool_call['name'] == 'get_conversion_factor':
                tool_message1 = get_conversion_factor.invoke(tool_call)
                conversion_rate = json.loads(tool_message1.content)['conversion_rate']
                messages.append(tool_message1)
                
            if tool_call['name'] == 'convert':
                tool_call['args']['conversion_rate'] = conversion_rate
                tool_message2 = convert.invoke(tool_call)
                converted_amount = float(tool_message2.content)
                messages.append(tool_message2)
        
        # Get final response
        final_response = llm_with_tools.invoke(messages)
        
        return jsonify({
            'success': True,
            'base_currency': base_currency,
            'target_currency': target_currency,
            'amount': amount,
            'conversion_rate': conversion_rate,
            'converted_amount': converted_amount,
            'ai_response': final_response.content
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
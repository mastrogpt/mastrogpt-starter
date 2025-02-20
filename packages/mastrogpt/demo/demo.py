USAGE = "Please type one of 'code', 'chess', 'html', 'form', 'message'"

FORM = [
  {
      "name": "why",
      "label": "Why do you recommend Apache OpenServerless?",
      "type": "textarea",
      "required": "true"
  },
  {
    "name": "job",
    "label": "What is your job role?",
    "type": "text",
    "required": "true"
  },
  {
    "name": "tone",
    "label": "What tone should the post have?",
    "type": "text",
    "required": "true"
  }
]

HTML = """<div class="max-w-md mx-auto p-6 bg-white shadow-md rounded-lg">
  <h1 class="text-2xl font-bold text-gray-800 mb-6">Sample Form</h1>
  <form action="/submit-your-form-endpoint" method="post" class="space-y-4">
    <div class="flex flex-col">
      <label for="username" class="mb-2 text-sm font-medium text-gray-700">Username:</label>
      <input
        type="text"
        id="username"
        name="username"
        required
        class="p-2 border border-gray-300 rounded-md bg-gray-200 text-black focus:ring-2 focus:ring-teal-500 focus:outline-none"
      />
    </div>
    <div class="flex flex-col">
      <label for="password" class="mb-2 text-sm font-medium text-gray-700">Password:</label>
      <input
        type="password"
        id="password"
        name="password"
        required
        class="p-2 border border-gray-300 rounded-md bg-gray-200 text-black focus:ring-2 focus:ring-teal-500 focus:outline-none"
      />
    </div>
    <div>
      <button
        type="submit"
        class="w-full py-2 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 focus:ring-2 focus:ring-blue-400 focus:outline-none"
      >
        Login
      </button>
    </div>
  </form>
</div>
"""

CODE = """
def sum_to(n):
    sum = 0
    for i in range(1,n+1):
        sum += i
    return sum
"""

CHESS = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"

import json

def demo(args):

    print(args)
        
    language = None
    code = None
    chess = None
    message = None
    html = None
    form = None
    title = None

    # initialize state
    try:
        # get the state if available
        counter = int(args.get("state")) +1
    except:
        # initialize the state
        counter = 1

    output = USAGE
    state = str(counter)    
    input = args.get("input", "")

    if type(input) is dict and "form" in input:
        data = input["form"]
        output = "FORM:\n"
        for field in data.keys():
          output += f"{field}: {data[field]}\n"
    elif input == "":
        output = f"Welcome to the Demo chat. {USAGE}"
    elif input == "code":
        code = CODE
        language = "python"
        output = f"Here is some python code.\n```python\n{code}\n```"
    elif input ==  "html":
        html = HTML
        output = f"Here is some HTML.\n```html\n{html}\n```"
    elif input == "message":
        message = "This is the message."
        title = "This is the title"
        output = "Here is a sample message."
    elif input == "form":
        output = "please fill the form"
        form = FORM
    elif input == "chess":
        chess = CHESS
        output = f"Check this chess position.\n\n{chess}"    
    else:
        output = f"You made {counter} requests. {USAGE}"
    
    # state is a counter incremented at any invocation
    res = {
        "output": output,
    }

    if state: res['state'] =  state
    if language: res['language'] = language
    if message: res['message'] =  message     
    if title: res['title'] = title
    if chess: res['chess'] = chess
    if code: res['code'] = code
    if html: res['html'] = html
    if form: res['form'] = form

    return res
# from flask import Flask, render_template, request
# import google.generativeai as genai

# app = Flask(__name__)
# genai.configure(api_key="AIzaSyBOgxan8GWoy78Ry2Ev2JnVY9PNkX_ljbs")  # Replace with your API key

# mymodel = genai.GenerativeModel("gemini-1.5-flash")
# chat = mymodel.start_chat()

# @app.route('/')
# def home():
#     return render_template('job_chat.html')  # Updated HTML filename

# @app.route('/send', methods=['POST', 'GET'])
# def submit():
#     uinput = request.form.get('user_input')
#     response = chat.send_message(f"Suggest job roles for skills: {uinput}")
#     return render_template('job_chat.html', user_input=uinput, message=response.text)

# if __name__ == "__main__":
#     app.run(debug=True)








from flask import Flask, render_template, request,redirect, url_for, flash,session
from werkzeug.security import check_password_hash
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = b'Ovp\xb7+I\xb2\xac\xf3$!1\x8e\xfd^[e0R\xa0s\xd9\xcc\xb5'
genai.configure(api_key="AIzaSyAzOTxpzYqxx1f4cpy-duUcqdughHlktAQ")  # Replace with your actual API key

mymodel = genai.GenerativeModel("gemini-1.5-flash")
chat = mymodel.start_chat()

# Predefined domains and subdomains
domains = {
    "Full-Stack Development": ["Front-End", "Back-End","MERN Stack", "MEAN Stack","Web Design","Web Security","DevOps"],
    "Data Science": ["Data Analysis","Machine Learning","Data Visualization","Big Data Analytics","Data Visualization", "Deep Learning","Natural Language Processing (NLP)","\n"],
    "Software Engineering":["Agile Development","DevOps","Software Testing","Cloud Computing","API Development"],
    "Digital Marketing":["Search Engine Optimization (SEO)","Social Media Marketing,Content Marketing","Email Marketing","Paid Advertising (PPC)"],
    "Graphic Design":["Logo Design","UI/UX Design","Illustration","Motion Graphics","Branding"],
    "Cybersecurity":["Network Security","Cryptography","Threat Analysis","Security Auditing","Incident Response"],
    "Mobile App Development":["iOS Development","Android Development","Cross-Platform Development","Mobile UX/UI Design","App Security"],
    "Cloud Computing":["Cloud Architecture","Cloud Security","Cloud Development","Cloud Migration","Serverless Computing"],
    "Artificial Intelligence":["Natural Language Processing (NLP)","Computer Vision","Deep Learning","Reinforcement Learning","Neural Networks"],
    "Finance":["Financial Modeling","Investment Analysis","Risk Management","Accounting","Financial Planning"],
    "Networking": ["CCNA", "CCNP", "Network Security", "Wireless Networking", "Network Troubleshooting"],
    "System Administration": ["Linux Administration", "Windows Server", "VMware", "Cloud Systems"],
    "Embedded Systems": ["Arduino", "Raspberry Pi", "FPGA Programming", "Microcontrollers", "C Programming"],
    "IoT": ["IoT Protocols", "IoT Security", "IoT Development Tools", "Smart Devices"],
    "Others": ["Marketing","Content Writing","HR","Sales"],
}

skills = {
    "Front-End": ["HTML/CSS", "JavaScript", "React", "Vue.js", " Angular","Responsive Design, Bootstrap","Version Control (Git)"],
    "Back-End": ["Node.js", "Django", "Flask", "Spring Boot","Ruby on Rails"],
    "MERN Stack": ["JavaScript(ES6+)", "MongoDB", "Express.js", "Node.js","React","Frontend Skills","Version Control","Deployment","Authentication and Security","Debugging and Testing"],
    "MEAN Stack": ["JavaScript(ES6+)", "MongoDB", "Express.js", "Node.js","Angular","Frontend Skills","Version Control","Deployment","Authentication and Security","Debugging and Testing"],
    "Web Design":["Graphic Design Tools (Photoshop, Figma)","UI/UX Principles","Wireframing & Prototyping","Typography & Color Theory","Web Accessibility"],
    "Web Security":["Cryptography","Web Application Firewalls (WAF)","SSL/TLS","Penetration Testing","Secure Coding Practices"],
    "DevOps": ["Docker, Kubernetes", "CI/CD Tools (Jenkins, Travis CI)", "Cloud Platforms (AWS, Azure, Google Cloud)", "Infrastructure as Code (Terraform, Ansible)"],
    "Data Analysis":["Data Cleaning & Wrangling","Excel / Google Sheets","SQL / NoSQL Databases","Data Visualization Tools (Tableau, Power BI)","Statistical Analysis (R, Python)"],
    "Machine Learning": ["Python","Scikit-learn","TensorFlow","Keras", "Model Evaluation",],
    "Data Visualization": ["Tableau","Power BI","Matplotlib","Seaborn", "Plotly"],
    "Big Data Analytics": ["Hadoop","Spark","SQL","NoSQL", "MapReduce"],
    "Deep Learning": ["Neural Networks","TensorFlow","PyTorch","CNN", "RNN"],
    "Natural Language Processing (NLP)": ["NLTK","SpaCy","Gensim","Text Preprocessing", "Sentiment Analysis"],
    "Agile Development":["Scrum / Kanban Methodologies","Agile Project Management Tools (Jira, Trello)","User Stories & Backlog Management","Continuous Integration & Delivery","Sprint Planning & Review"],
    "Software Testing":["Manual Testing Techniques","Automated Testing(Selenium, JUnit)","Test-Driven Development(TDD)","Bug Tracking Tools (Jira)","Regression Testing"],
    "Cloud Computing":["Cloud Services (AWS, Azure, GCP)","Virtualization (VMware, Hyper-V)","Cloud Security","Cloud Storage Solutions","DevOps Automation in the Cloud"],
    "API Development":["RESTful API Design","API Authentication (OAuth, JWT)","API Testing (Postman, Swagger)","Rate Limiting & Versioning","Error Handling & Logging"],
    "SEO":["Keyword Research","On-Page SEO (Meta Tags, Content Optimization)","Link Building","SEO Analytics (Google Analytics, Search Console)","Technical SEO (Site Speed, Mobile Optimization)"],
    "Social Media Marketing":["Content Creation","Social Media Strategy","WindowsErrorPaid Campaign Management (Facebook Ads, Google Ads)","Social Media Analytics (Hootsuite, Sprout Social"],
    "Community Engagement":["Content Marketing","Content Strategy","Copywriting","Blogging & Article Writing","Content Distribution Channels","SEO Content Writing"],
    "Email Marketing": ["Content Distribution Channels","SEO Content Writing","Email Campaign Design","List Building & Segmentation","A/B Testing"],
    "PPC Advertising":["Keyword Research","Google Ads (Search, Display)","Campaign Optimization","Ad Copywriting","Performance Tracking",],
    "Logo Design":["Adobe Illustrator","Typography","Color Theory","Brand Identity","Vector Illustration"],
    "UI/UX Design":["User Research & Personas","Prototyping (Figma, Sketch)","Wireframing","Interaction Design","Usability Testing"],
    "Illustration":["Adobe Photoshop / Illustrator","Digital Drawing Techniques","Composition & Layout","Character Design","Storyboarding"],
    "Motion Graphics":["Adobe After Effects","Animation Techniques","Video Editing""Sound Design","Storytelling in Animation"],
    "Branding":["Brand Strategy""Visual Identity","Brand Positioning","Market Research","Brand Consistency"],







    
    "Product Design": ["3D Modeling", "SolidWorks", "AutoCAD", "3D Printing"],
    "Content Writing": ["Blog Writing", "Technical Writing", "Creative Writing", "Copywriting"],
    "HR": ["Recruitment", "Payroll Management", "Employee Engagement", "Conflict Resolution"],
    "Sales": ["B2B Sales", "B2C Sales", "CRM Tools", "Cold Calling"]
}


users_db= {
    'testuser': {
        'password': 'hashed_password_here',
    }           # Example additional user
}

@app.route('/')
def welcome():
    return render_template('index.html')
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    if username in users_db:
            # Verify the password (assuming you're using hashed passwords)
        if check_password_hash(users_db[username]['password'], password):
            session['username'] = username  # Store username in the session to keep track of the login
            flash('Login successful!', 'success')
            return redirect(url_for('start'))
    else:
        flash("Invalid credentials. Please try again.", "error")
    return redirect(url_for('welcome'))

@app.route('/register')
def register():
    # Placeholder for registration logic
    return "Registration Page (coming soon)"

@app.route('/start')
def start():
    return render_template('job_chat.html', domains=domains.keys())

@app.route('/domain', methods=['POST'])
def get_subdomains():
    user_domain = request.form.get('domain')
    subdomains = domains.get(user_domain, [])
    return render_template('job_chat.html', user_domain=user_domain, subdomains=subdomains)

@app.route('/subdomain', methods=['POST'])
def get_skills():
    user_domain = request.form.get('user_domain')
    user_subdomain = request.form.get('subdomain')
    skill_options = skills.get(user_subdomain, [])
    return render_template('job_chat.html', user_domain=user_domain, user_subdomain=user_subdomain, skills=skill_options)

@app.route('/recommend', methods=['POST'])
def recommend_jobs():
    user_domain = request.form.get('user_domain')
    user_subdomain = request.form.get('user_subdomain')
    user_skills = request.form.getlist('skills')

    # Generate tailored recommendations
    prompt = (
        f"The user is interested in {user_domain}, specifically {user_subdomain}. "
        f"They are skilled in {', '.join(user_skills)}. "
        " Generate 5 job recommendations tailored to these skills. Suggest additional skills and resources for upskilling."
    )
    response = chat.send_message(prompt)

    # Clean and format the response for better readability
    recommendations = response.text.strip().split("\n")
    # recommendations = [line.strip() for line in recommendations if line.strip()]

    # Pass structured recommendations to the template
    return render_template(
        'job_chat.html',
        user_domain=user_domain,
        user_subdomain=user_subdomain,
        user_skills=user_skills,
        message=recommendations
    )



if __name__ == "__main__":
    app.run(debug=True)



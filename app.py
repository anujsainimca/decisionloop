import streamlit as st
import moviepy.editor as mp
import docx
from openai import OpenAI
import tempfile 

st.title("Decision Loop")

# Get OpenAI API key from user input
api_key = st.text_input("Enter your OpenAI API key", type="password")
client = OpenAI(api_key=api_key)

# Upload video file
video_file = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi"])

# Upload Word document
doc_file = st.file_uploader("Upload a Word Document", type=["docx"])
system_prompt="You are a Change Management Consultant or Organizational Development Consultant help companies to take decision using employees feedback for a technology or functional proposed change. Provide a detailed report for given change and employees feedback to help companies"

prompt='The AI system should measure by scoring the level of awareness a stakeholder has about an organizational change. The AI system should also provide recommendations for actions to take based on the score given. Use the following Likert Scale to generate a report. Responses that are similar to "I am not aware of the new product, system or business processes change or why they are needed" should be given a score of 1. Responses that are similar to "I have some awareness of the new product, system or business process changes or why they are needed" should be given a score of 5. Responses that are similar to "I am highly aware of the new product, system or business process changes or why they are needed" should be given a score of 10. Write a communication, training, and engagement recommendation for each score. Start the analysis with "Based on the response provided, the Level of awareness is considered ___"'

few_shot_examples="""
Report: Stakeholder Awareness and Recommendations
Response: "I am not aware of the new product, system, or business process change or why they are needed."
Analysis Report: Based on the response provided, the Level of awareness is considered Low.
Recommendations:
Communication:
Launch an initial communication campaign to introduce the change.
Use multiple channels (emails, intranet announcements, posters) to ensure broad reach.
Clearly explain the reasons for the change and the benefits it will bring to the organization.
Training:
Develop and distribute basic informational materials (FAQs, brochures) explaining the change.
Offer introductory webinars or presentations to provide an overview of the new product/system/process.
Engagement:
Hold town hall meetings or Q&A sessions where stakeholders can ask questions and express concerns.
Identify and engage early adopters to act as change champions who can help spread awareness.
Response: "I have some awareness of the new product, system, or business process changes or why they are needed."
Analysis Report: Based on the response provided, the Level of awareness is considered Moderate.
Recommendations:
Communication:
Provide detailed updates on the change process and timelines.
Share success stories and testimonials from early adopters or pilot users.
Use newsletters and regular email updates to keep stakeholders informed.
Training:
Offer more in-depth training sessions, including hands-on workshops and detailed tutorials.
Create a knowledge base or resource center with comprehensive guides, video tutorials, and troubleshooting tips.
Engagement:
Conduct focus groups to gather feedback and address specific concerns.
Encourage stakeholders to participate in pilot programs or beta testing phases to increase familiarity and comfort with the change.
Establish a support network or forum where stakeholders can share experiences and solutions.
Response: "I am highly aware of the new product, system, or business process changes or why they are needed."
Analysis Report: Based on the response provided, the Level of awareness is considered High.
Recommendations:
Communication:
Recognize and celebrate stakeholders who are fully aware and supportive of the change.
Share advanced insights and strategic benefits of the change to maintain engagement.
Use these stakeholders as case studies or testimonials to further promote the change.
Training:
Provide advanced training sessions and certification programs for deeper expertise.
Offer opportunities for stakeholders to lead training sessions or mentor others.
Develop specialized content that addresses advanced features and best practices.
Engagement:
Involve highly aware stakeholders in decision-making processes and implementation planning.
Form advisory groups or committees to leverage their knowledge and experience.
Encourage them to take on ambassador roles to advocate for the change and assist less aware colleagues.
"""

metric="""

USER READINESS CHECKLIST - ASSESSMENT CRITERIA
When to use: The survey should be used as part of a User Readiness Checklist.



METRIC
LIKERT SCALE FOR SCORING RESPONSES

QUESTION TO ASK
DECISIONLOOP WILL GENERATE BASED ON THE LIKERT SCALE
1
2-4
5
6-9
10
Sentiment
Negative


Neutral


Positive
Describe your attitude toward the organizational change. Explain the reason for your response.


Level of Awareness
I am not aware of the new product, system or business processes chang or why they are needed


I have some awareness of the new product, system or business process changes or why they are needed


I am highly aware of the new product, system or business process changes or why they are needed
Based on what you know, describe your level of awareness of the new system being implemented and why it is needed?
This report aims to ensure that stakeholders at all levels of awareness receive the appropriate support to facilitate a smooth transition to new products, systems, or business processes. By tailoring communication, training, and engagement strategies to their awareness levels, organizations can enhance overall readiness and adoption of changes.
Perception of Usefulness	
I do not feel the new product, system or business processes is beneficial and useful to my job tasks


I somewhat feel the new product, system or business process is beneficial and useful to my job tasks


I highly feel the new product, system, or process is beneficial and useful to my job tasks
Based on what you know, describe your perception of how beneficial  or useful you think the new technology system will be to your daily job tasks. Is it useful?


Perception of Ease of Use	
I do not feel the new product, system or business processes is easy for me to use


I somewhat feel the new product, system or business processes is easy for me to use


I highly feel the new product, system or business processes is easy for me to use




Level of Intention	
I do not intend to use the new product, system or business processes


I am undecided about my intention to use the new product, system or business processes


I fully intend to use the new product, system or business processes




Level of Motivation
I am not motivated to begin using the new product, system or business processes


I am somewhat motivated to begin using the new product, system or business processes


I am highly motivated to begin using the new product, system or busienss processes




Level of Willingness
I am not willing to adopt the new product, system or business processes


I am somewhat willing to adopt the new product, system or business processes


I am fully willing to adopt the new product system or business processes




Level of Ability
I do not have the skills needed to use the new system, or busineess processes


I am somewhat skilled to use the new product, system, or business processes


I am fully skilled and able to use the new product, system, or business processes




Level of Confidence (Trust)
I do not have confidence and trust in the business culture or leadership's commitment to drive the change


I have some confidence and trust in the business culture or leadership's commitment to drive the change


I have full confidence and trust in the business culture or leadership's commitment to drive the change




Level of Satisfaction
I am not satisfied and comfortable that the change will work as designed.


I am somewhat satisfied and comfortable that the change will work as designed.


I am fully satisfied and comfortable that the change will work as designed.


"""

if video_file and doc_file:
    st.success("Files uploaded successfully!")
    
    # Create a temporary file to save the uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(video_file.read())
        video_path = tmp_video.name

    # Convert video to audio (mp3)
    video = mp.VideoFileClip(video_path)
    audio_path = "audio.mp3"
    video.audio.write_audiofile(audio_path, buffersize=4000)

    # Recognize speech from the audio
    with open(audio_path, "rb") as audio_file:
        extracted_text = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )

    st.write("Extracted Text from Video:")
    st.write(extracted_text)

    # Read the Word document and extract text
    doc = docx.Document(doc_file)
    doc_text = "\n".join([para.text for para in doc.paragraphs])

    st.write("Processing Feedback...")

    # Constructing the prompt
    final_prompt=prompt+"\nQuestion: "+extracted_text+"\n"+few_shot_examples+"\n"+metric+"\n. Responses: "+doc_text

    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": final_prompt}
      ]
    )
    
    st.markdown(
    "<h2 style='color: red;'>Generated Report:</h2>", 
    unsafe_allow_html=True)
    st.write(completion.choices[0].message.content)
else:
    st.info("Please upload both a video file and a Word document to proceed.")

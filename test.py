import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

st.title("Intelligent Data-Visualization Tool")

# Welcome message
with st.chat_message('ai'):
    st.markdown("Hello! Welcome to the Intelligent Data Visualization Tool. Upload your dataset to continue.")

# File uploader to handle both CSV and Excel files
content = st.file_uploader("Upload your CSV/Excel file", type=['csv', 'xlsx'])

if content is not None:
    try:
        # Check file type and read the appropriate file
        if content.name.endswith('.csv'):
            df = pd.read_csv(content)
        elif content.name.endswith('.xlsx'):
            df = pd.read_excel(content)
        
        # Display the DataFrame
        st.write(df)

        # Extract column names for dropdown menus
        columns = df.columns.tolist()

        # Create dropdown menus for selecting x-axis and y-axis
        x_axis = st.selectbox("Select X-axis", options=columns)
        y_axis = st.selectbox("Select Y-axis", options=columns)

        st.write(f"Selected X-axis: {x_axis}")
        st.write(f"Selected Y-axis: {y_axis}")

        # Groq API setup
        client = Groq(api_key="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")

        # Request to Groq API to determine the best graph type
        if st.button("Recommend Graph"):
            prompt = f"Based on the given x-axis '{x_axis}' and y-axis '{y_axis}', what is the most suitable graph type for visualizing the data? available graphs [line,bar,scatter,pie] provide only one word answer"
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            graph_recommendation = response.choices[0].message.content
            st.write(f"Recommended Graph Type: {graph_recommendation}")

            # Plot the graph based on the recommendation
            if graph_recommendation.lower() == "bar":
                fig = px.bar(df, x=x_axis, y=y_axis, title=f"Bar Chart: {x_axis} vs {y_axis}")
            elif graph_recommendation.lower() == "line":
                fig = px.line(df, x=x_axis, y=y_axis, title=f"Line Chart: {x_axis} vs {y_axis}")
            elif graph_recommendation.lower() == "scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
            elif graph_recommendation.lower() == "pie":
                fig = px.pie(df, names=x_axis, values=y_axis, title=f"Pie Chart: {y_axis} by {x_axis}")
            else:
                st.write("Unsupported graph type. Please select a different type.")

            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {e}")

# Initialize message history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input and process Groq API response
# if prompt := st.chat_input("What's on your mind?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Call Groq API
#     with st.chat_message("assistant"):
#         response = client.chat.completions.create(
#             model=st.session_state["groq_model"],
#             messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
#         )
#         assistant_message = response.choices[0].message.content
#         st.markdown(assistant_message)

#     # Add assistant's response to session state
#     st.session_state.messages.append({"role": "assistant", "content": assistant_message})

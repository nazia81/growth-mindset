import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Growth Mindset Challenge",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'challenges_completed' not in st.session_state:
    st.session_state.challenges_completed = 0
if 'reflections' not in st.session_state:
    st.session_state.reflections = []
if 'last_challenge_date' not in st.session_state:
    st.session_state.last_challenge_date = None
if 'streak' not in st.session_state:
    st.session_state.streak = 0

# Growth mindset challenges database
challenges = [
    "Try a new approach to a problem you've been struggling with",
    "Ask for feedback on your work and reflect on it constructively",
    "Teach someone else a concept you're learning",
    "Set a challenging goal and break it down into smaller steps",
    "Embrace a mistake as a learning opportunity",
    "Visualize yourself succeeding after multiple attempts",
    "Replace 'I can't' statements with 'I can't yet'",
    "Identify three things you learned from a recent failure",
    "Practice self-compassion when facing difficulties",
    "Celebrate small progress along your journey"
]

# Motivational quotes
quotes = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "I have not failed. I've just found 10,000 ways that won't work. - Thomas Edison",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
    "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The way to get started is to quit talking and begin doing. - Walt Disney"
]

# Sidebar
with st.sidebar:
    st.title("🌱 Growth Mindset Challenge")
    st.write("Develop a growth mindset through daily challenges and reflections.")
    
    # Display streak
    st.metric("Current Streak", f"{st.session_state.streak} days")
    
    # Display total challenges completed
    st.metric("Challenges Completed", st.session_state.challenges_completed)
    
    # Navigation
    st.write("## Navigation")
    page = st.radio("Go to", ["Today's Challenge", "Reflection Journal", "Progress Stats"])

# Main content
if page == "Today's Challenge":
    st.title("Today's Growth Mindset Challenge")
    
    # Check if user has already completed today's challenge
    today = datetime.now().date()
    if st.session_state.last_challenge_date == today:
        st.success("You've already completed today's challenge! Come back tomorrow for a new one.")
        st.write("### Today's Challenge (Completed)")
        st.info(challenges[0])  # Show the same challenge for consistency
    else:
        # Select a random challenge
        today_challenge = random.choice(challenges)
        st.write("### Your Challenge for Today")
        st.info(today_challenge)
        
        # Challenge completion
        if st.button("I Completed This Challenge"):
            st.session_state.challenges_completed += 1
            st.session_state.last_challenge_date = today
            
            # Update streak
            if st.session_state.last_challenge_date is not None:
                yesterday = today - timedelta(days=1)
                if st.session_state.last_challenge_date == yesterday:
                    st.session_state.streak += 1
                elif st.session_state.last_challenge_date != today:
                    st.session_state.streak = 1
            else:
                st.session_state.streak = 1
                
            st.success("Great job! Challenge completed. Your streak and progress have been updated.")
            st.balloons()
    
    # Display a random motivational quote
    st.write("### Daily Inspiration")
    st.write(f"*{random.choice(quotes)}*")

elif page == "Reflection Journal":
    st.title("Reflection Journal")
    
    # Add new reflection
    st.write("### Add a New Reflection")
    reflection_text = st.text_area("What did you learn from today's challenge?")
    reflection_date = st.date_input("Date", datetime.now())
    
    if st.button("Save Reflection"):
        if reflection_text:
            st.session_state.reflections.append({
                "date": reflection_date,
                "text": reflection_text
            })
            st.success("Reflection saved successfully!")
            st.experimental_rerun()
        else:
            st.error("Please enter a reflection before saving.")
    
    # Display past reflections
    st.write("### Past Reflections")
    if st.session_state.reflections:
        for i, reflection in enumerate(reversed(st.session_state.reflections)):
            with st.expander(f"Reflection from {reflection['date']}"):
                st.write(reflection['text'])
    else:
        st.info("No reflections yet. Start by adding your first reflection!")

elif page == "Progress Stats":
    st.title("Your Progress Statistics")
    
    # Create a simple progress visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Challenge Completion")
        st.metric("Total Challenges Completed", st.session_state.challenges_completed)
        
        # Create a simple bar chart for the last 7 days
        if st.session_state.last_challenge_date:
            dates = [(datetime.now() - timedelta(days=i)).date() for i in range(7)]
            completed = [1 if date == st.session_state.last_challenge_date else 0 for date in dates]
            
            chart_data = pd.DataFrame({
                'Date': dates,
                'Completed': completed
            })
            
            st.bar_chart(chart_data.set_index('Date'))
    
    with col2:
        st.write("### Current Streak")
        st.metric("Days in a Row", st.session_state.streak)
        
        # Display streak visualization
        streak_data = pd.DataFrame({
            'Day': range(1, st.session_state.streak + 1),
            'Value': [1] * st.session_state.streak
        })
        
        if not streak_data.empty:
            st.line_chart(streak_data.set_index('Day'))
        else:
            st.info("Complete challenges to start building your streak!")
    
    # Reflection statistics
    st.write("### Reflection Statistics")
    st.metric("Total Reflections", len(st.session_state.reflections))
    
    # Display a random quote for motivation
    st.write("### Keep Going!")
    st.write(f"*{random.choice(quotes)}*")

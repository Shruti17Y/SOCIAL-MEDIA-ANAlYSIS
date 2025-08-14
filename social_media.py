import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Social Media Analysis", layout="wide")

# Define Social Media Platforms with Logos
social_media_options = {
    "Instagram": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png",
    "Twitter": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Logo_of_Twitter.svg", 
    "Facebook": "https://upload.wikimedia.org/wikipedia/commons/0/05/Facebook_Logo_%282019%29.png",
    "Snapchat": "snapchat-logo.png",  
    "YouTube": "https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg"
}  

st.title("📊 Social Media Usage Analysis Dashboard")
st.write("")
st.write("")


@st.cache_data
def load_data():
    try:
        data = pd.read_csv("Social_media_analysis_sorted.csv")
        # Normalize the 'Country' and 'App' columns
        data["Country"] = data["Country"].str.strip().str.lower()
        data["App"] = data["App"].str.strip().str.lower()
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

data = load_data()


if "step" not in st.session_state:
    st.session_state.step = 1

# Step 1:
if st.session_state.step == 1:
    st.markdown("### Choose Social Media Apps :")
    st.write("")
    st.write("")
    
    cols = st.columns(len(social_media_options))
    selected_apps = []
    for i, (app, logo) in enumerate(social_media_options.items()):
        with cols[i]:
            st.image(logo, width=50)
            if st.checkbox(app, key=app):
                selected_apps.append(app.strip().lower())  # Normalize selected apps

    st.write("") 

    # Display the "Next" button 
    if selected_apps:
        st.session_state.selected_apps = selected_apps
        if st.button("Next ➡️"):
            st.session_state.step = 2
            st.rerun()

   
    st.markdown("### Summary of Social Media Apps :")
    st.write("") 
    st.write("")
    st.markdown("#### Likes vs App (Pie Chart)")
    st.write("") 
    
    summary_data = data[data["App"].str.strip().str.lower().isin([app.lower() for app in social_media_options.keys()])]

    likes_by_app = summary_data.groupby("App", as_index=False)["Likes"].sum()
    
    if not likes_by_app.empty:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            fig, ax = plt.subplots(figsize=(6, 6))
            colors = sns.color_palette("pastel", len(likes_by_app))
            wedges, texts, autotexts = ax.pie(
                likes_by_app["Likes"], 
                labels=likes_by_app["App"], 
                autopct="%1.1f%%", 
                startangle=90, 
                colors=colors, 
                wedgeprops={"edgecolor": "white", "linewidth": 1.5},
                textprops={"fontsize": 12}
            )
            ax.axis("equal")
            plt.title("Proportion of Likes by Social Media App", fontsize=14, fontweight='bold', pad=20)
            st.pyplot(fig, use_container_width=False)
    else:
        st.warning("No data available for the social media apps.")

    st.write("")

    # 1. App vs Time Spent (Bar Chart)
    st.markdown("#### App vs Time Spent (Bar Chart)")
    st.write("")
    time_spent_by_app = summary_data.groupby("App", as_index=False)["time_spent"].sum()
    if not time_spent_by_app.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=time_spent_by_app, x="App", y="time_spent", ax=ax, palette="viridis")
        plt.title("Time Spent by Social Media App", fontsize=16, fontweight='bold')
        plt.xlabel("App", fontsize=14)
        plt.ylabel("Time Spent (minutes)", fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        for p in ax.patches:
            ax.annotate(f"{int(p.get_height())}", 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', 
                        xytext=(0, 10), 
                        textcoords='offset points',
                        fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7, axis='y')
        st.pyplot(fig, use_container_width=True)
    else:
        st.warning("No data available for Time Spent by App.")

    # 2. Country vs App (Scatter Plot)
    st.markdown("#### Country vs App (Scatter Plot)")
    st.write("")
    if not summary_data.empty:
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.scatterplot(
            data=summary_data, 
            x="Country", 
            y="App", 
            hue="App", 
            ax=ax, 
            palette="plasma",
            s=150
        )
        plt.title("Country vs App Usage", fontsize=16, fontweight='bold')
        plt.xlabel("Country", fontsize=14)
        plt.ylabel("App", fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=12)
        st.pyplot(fig, use_container_width=True)
    else:
        st.warning("No data available for Country vs App.")

    # 3. Usage Duration vs App (Line Graph)
    st.markdown("#### Usage Duration vs App (Line Graph)")
    st.write("")
    if not summary_data.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(
            data=summary_data, 
            x="App", 
            y="UsageDuration", 
            hue="App", 
            ax=ax, 
            palette="magma",
            marker="o",  
            linewidth=2.5  
        )
        plt.title("Usage Duration by App (Line Graph)", fontsize=16, fontweight='bold')
        plt.xlabel("App", fontsize=14)
        plt.ylabel("Usage Duration (minutes)", fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=12)
        st.pyplot(fig, use_container_width=True)
    else:
        st.warning("No data available for Usage Duration vs App.")

    # 4. User ID vs App (Box Plot)
    st.markdown("#### User ID vs App (Box Plot)")
    st.write("")
    if not summary_data.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(
            data=summary_data, 
            x="App", 
            y="Userid", 
            ax=ax, 
            palette="Set3",
            width=0.6,
            showfliers=False
        )
        
        plt.title("User ID Distribution by App", fontsize=16, fontweight='bold')
        plt.xlabel("App", fontsize=14)
        plt.ylabel("User ID", fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7, axis='y')
        st.pyplot(fig, use_container_width=True)
    else:
        st.warning("No data available for User ID vs App.")

# Step 2: 
if st.session_state.step == 2:
    st.sidebar.header("Enter Required Inputs")
    
    
    unique_countries = data["Country"].drop_duplicates().sort_values().tolist()
    selected_country = st.sidebar.selectbox("🌍 Select Country:", unique_countries)

    graph_types = {}
    for app in st.session_state.selected_apps:
        st.sidebar.markdown(f"### {app} Graph Options")
        
      
        graph_type_options = ["User vs Likes", "Year vs Likes", "Search for You 🔍"]
        graph_type = st.sidebar.selectbox(
            f"Choose a graph type for {app}:",
            graph_type_options,
            key=f"graph_type_{app}"
        )
        
       
        if graph_type == "Search for You 🔍":
            st.sidebar.markdown(f"#### 🔧 Custom Graph Options for {app}")
            custom_graph_type = st.sidebar.selectbox(
                f"Select Graph Type for {app} 📊:",
                ["Bar Plot", "Pie Chart", "Scatter Plot", "Histogram"],
                key=f"custom_graph_type_{app}"
            )
            x_axis = st.sidebar.selectbox(
                f"Select X-axis for {app} 📌:",
                data.columns,
                key=f"x_axis_{app}"
            )
           
            if custom_graph_type in ["Bar Plot", "Scatter Plot"]:
               
                if custom_graph_type == "Bar Plot":
                    numerical_columns = data.select_dtypes(include=['int', 'float']).columns.tolist()
                    y_axis = st.sidebar.selectbox(
                        f"Select Y-axis for {app} 📌:",
                        numerical_columns,
                        key=f"y_axis_{app}"
                    )
                else:  
                    y_axis = st.sidebar.selectbox(
                        f"Select Y-axis for {app} 📌:",
                        data.columns,
                        key=f"y_axis_{app}"
                    )
            else:
                y_axis = None
            graph_types[app] = {
                "graph_type": custom_graph_type,
                "x_axis": x_axis,
                "y_axis": y_axis
            }
        else:
            
            graph_types[app] = {
                "graph_type": graph_type,
                "x_axis": graph_type.split(" vs ")[0],
                "y_axis": graph_type.split(" vs ")[1]
            }

   
    if st.sidebar.button("📈 Show the Graph"):
        
        filtered_data = data[
            (data["Country"].str.strip().str.lower() == selected_country.strip().lower()) & 
            (data["App"].str.strip().str.lower().isin(st.session_state.selected_apps))
        ]
        
        if not filtered_data.empty:
            for app in st.session_state.selected_apps:
                st.subheader(f"📊 {app} in {selected_country}")
                st.write("")
                fig, ax = plt.subplots(figsize=(12, 6))
                
               
                graph_type = graph_types[app]["graph_type"]
                x_axis = graph_types[app]["x_axis"]
                y_axis = graph_types[app]["y_axis"]
                
                
                if x_axis not in data.columns:
                    st.error(f"Invalid X-axis selection for {app}. Please select a valid column.")
                    continue
                if graph_type not in ["Pie Chart", "Histogram"] and (y_axis not in data.columns):
                    st.error(f"Invalid Y-axis selection for {app}. Please select a valid column.")
                    continue
                
                
                if graph_type == "Bar Plot":
                    sns.barplot(
                        data=filtered_data[filtered_data["App"].str.strip().str.lower() == app], 
                        x=x_axis, 
                        y=y_axis, 
                        ci=None,
                        ax=ax, 
                        palette="coolwarm"
                    )
                    plt.title(f"{x_axis} vs {y_axis} for {app}", fontsize=16, fontweight='bold')
                    plt.xlabel(x_axis, fontsize=14)
                    plt.ylabel(y_axis, fontsize=14)
                    plt.xticks(rotation=45, ha='right', fontsize=12)
                    for p in ax.patches:
                        ax.annotate(f"{int(p.get_height())}", 
                                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                                    ha='center', va='center', 
                                    xytext=(0, 10), 
                                    textcoords='offset points',
                                    fontsize=12)
                    plt.grid(True, linestyle='--', alpha=0.7)
                
                elif graph_type == "Pie Chart":
                   
                    pie_data = filtered_data[filtered_data["App"].str.strip().str.lower() == app][x_axis].value_counts()
                    ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90, 
                           colors=sns.color_palette("Set3"), textprops={"fontsize": 12})
                    ax.axis("equal")
                    plt.title(f"Distribution of {x_axis} for {app}", fontsize=16, fontweight='bold', pad=20)
                
                elif graph_type == "Scatter Plot":
                    sns.scatterplot(
                        data=filtered_data[filtered_data["App"].str.strip().str.lower() == app], 
                        x=x_axis, 
                        y=y_axis, 
                        ax=ax, 
                        palette="viridis", 
                        s=100
                    )
                    plt.title(f"{x_axis} vs {y_axis} for {app}", fontsize=16, fontweight='bold')
                    plt.xlabel(x_axis, fontsize=14)
                    plt.ylabel(y_axis, fontsize=14)
                    plt.xticks(rotation=45, ha='right', fontsize=12)
                    plt.grid(True, linestyle='--', alpha=0.7)
                    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=12)
                
                elif graph_type == "Histogram":
               
                    sns.histplot(
                        data=filtered_data[filtered_data["App"].str.strip().str.lower() == app][x_axis], 
                        kde=True, 
                        ax=ax, 
                        color="skyblue", 
                        edgecolor="black"
                    )
                    plt.title(f"Distribution of {x_axis} for {app}", fontsize=16, fontweight='bold')
                    plt.xlabel(x_axis, fontsize=14)
                    plt.ylabel("Frequency", fontsize=14)
                    plt.xticks(rotation=45, ha='right', fontsize=12)
                    plt.grid(True, linestyle='--', alpha=0.7)
                
                else:
                    
                    if graph_type == "User vs Likes":
                        sns.barplot(
                            data=filtered_data[filtered_data["App"].str.strip().str.lower() == app], 
                            x="User", 
                            y="Likes", 
                            hue="User", 
                            ax=ax, 
                            palette="Set2"
                        )
                        plt.title("User vs Likes", fontsize=16, fontweight='bold')
                        plt.xlabel("User", fontsize=14)
                        plt.ylabel("Likes", fontsize=14)
                        plt.xticks(rotation=45, ha='right', fontsize=12)
                        plt.grid(True, linestyle='--', alpha=0.7)
                    
                    
                    elif graph_type == "Year vs Likes":
                        sns.barplot(
                            data=filtered_data[filtered_data["App"].str.strip().str.lower() == app], 
                            x="Year", 
                            y="Likes", 
                            hue="Year", 
                            ax=ax, 
                            palette="Set2"
                        )
                        plt.title("Year vs Likes", fontsize=16, fontweight='bold')
                        plt.xlabel("Year", fontsize=14)
                        plt.ylabel("Likes", fontsize=14)
                        plt.xticks(rotation=45, ha='right', fontsize=12)
                        plt.grid(True, linestyle='--', alpha=0.7)
                
                plt.tight_layout()
                st.pyplot(fig)
        else:
            st.warning("No matching data found! Try adjusting filters.")
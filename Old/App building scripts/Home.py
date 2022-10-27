import linkedinAPI
import streamlit as st
from streamlit.components.v1 import html


@st.cache
def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elapsed = new Date() - start_time;
                if (elapsed < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)


st.title("ESG Glassdoor")

st.write("Raising transparency on companies' attitude towards ESG and compare their position with public perception.")


col1, col2, col3 = st.columns(3)
with col1:
    company_name = st.selectbox("Company", (list(linkedinAPI.getPosts().company.unique())), index=3)
with col2:
    since_date = st.text_input("Get posts since", value="YYYY-MM-DD")
with col3:
    linkedin_count = st.slider("Max LinkedIn posts", min_value=100, max_value=1000, step=10, value=0) 

keywords = st.multiselect(
    'Hashtags',
    ['#sustainability', '#marketing', '#carbon', '#religion', '#engineering', '#datascience'])

since_date = since_date[:7] + '--' + since_date[8:]

col1, col2, col3, col4 = st.columns(4)
with col2:
    company_analysis = st.button('Analyse this Company')
with col3:
    post_analysis = st.button('Try out your own Posts')


if company_analysis:
    nav_page("Company_Analysis")
if post_analysis:
    nav_page("Post_Analysis")
 
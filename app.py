import streamlit as st
import pandas as pd 
from db_fxns import * 
import streamlit.components.v1 as stc
import plost



# Data Viz Pkgs
import plotly.express as px 


HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App (CRUD)</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """


def main():
	stc.html(HTML_BANNER)


	menu = ["Create","Read","Update","Delete","admin","About"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()

	if choice == "Create":
		st.subheader("Add Item")
		col1,col2 = st.columns(2)
		
		with col1:
			task = st.text_area("Task To Do")

		with col2:
			task_status = st.selectbox("Status",["ToDo","Doing","Done"])
			task_due_date = st.date_input("Due Date")

		if st.button("Add Task"):
			add_data(task,task_status,task_due_date)
			st.success("Added ::{} ::To Task".format(task))


	elif choice == "Read":
		# st.subheader("View Items")
		with st.expander("View All"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		with st.expander("Task Status"):
			task_df = clean_df['Status'].value_counts().to_frame()
			# st.dataframe(task_df)
			task_df = task_df.reset_index()
			st.dataframe(task_df)

			p1 = px.pie(task_df,names='index',values='Status')
			st.plotly_chart(p1,use_container_width=True)


	elif choice == "Update":
		st.subheader("Edit Items")
		with st.expander("Current Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Task",list_of_tasks)
		task_result = get_task(selected_task)
		# st.write(task_result)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			col1,col2 = st.columns(2)
			
			with col1:
				new_task = st.text_area("Task To Do",task)

			with col2:
				new_task_status = st.selectbox(task_status,["ToDo","Doing","Done"])
				new_task_due_date = st.date_input(task_due_date)

			if st.button("Update Task"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Updated ::{} ::To {}".format(task,new_task))

			with st.expander("View Updated Data"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
				st.dataframe(clean_df)


	elif choice == "Delete":
		st.subheader("Delete")
		with st.expander("View Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Select Task",unique_list)
		if st.button("Delete"):
			delete_data(delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))

		with st.expander("Updated Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)
	elif choice=='admin':
		with open('style.css') as f:
			st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
		st.sidebar.header('Dashboard ')

		
		time_hist_color = st.sidebar.selectbox('`Color by`', ('temp_min', 'temp_max')) 

		st.sidebar.subheader('Donut chart parameter')
		donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

		st.sidebar.subheader('Line chart parameters')
		plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
		plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

		
		


		# Row A
		st.markdown('### Metrics')
		col1, col2, col3 = st.columns(3)
		col1.metric("Temperature", "70 °F", "1.2 °F")
		col2.metric("Wind", "9 mph", "-8%")
		col3.metric("Humidity", "86%", "4%")

		# Row B
		seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
		stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

		c1, c2 = st.columns((7,3))
		with c1:
			st.markdown('### Heatmap')
			plost.time_hist(
			data=seattle_weather,
			date='date',
			x_unit='week',
			y_unit='day',
			color=time_hist_color,
			aggregate='median',
			legend=None,
			height=345,
			use_container_width=True)
		with c2:
			st.markdown('### Donut chart')
			plost.donut_chart(
				data=stocks,
				theta=donut_theta,
				color='company',
				legend='bottom', 
				use_container_width=True)

		# Row C
		st.markdown('### Line chart')
		st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)

	else:
		contact_form = """
		<form action="https://formsubmit.co/haitranvipqt@gmail.com" method="POST">
			<input type="hidden" name="_captcha" value="false">
			<input type="text" name="name" placeholder="Your name" required>
			<input type="email" name="email" placeholder="Your email" required>
			<textarea name="message" placeholder="Your message here"></textarea>
			<button type="submit">Send</button>
		</form>
		"""

		st.markdown(contact_form, unsafe_allow_html=True)

		# Use Local CSS File
		def local_css(file_name):
			with open(file_name) as f:
				st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


		local_css("style.css")


if __name__ == '__main__':
	main()


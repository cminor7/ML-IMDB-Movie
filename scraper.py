import os
from collections import Counter
from statistics import *
import time
from selenium import webdriver

import cleaner as cl
import ld as ld
import classifier as clf

class IMDB:

	def __init__(self, name, year):

		# check what operating system user is on
		if os.name == 'nt': # Windows
			path = os.getcwd() + '/geckodriver.exe'
		else: # Mac
			path = os.getcwd() + '/geckodriver'

		# disable images
		firefox_profile = webdriver.FirefoxProfile()
		firefox_profile.set_preference('permissions.default.image', 2)
		firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
		
		self.driver = webdriver.Firefox(executable_path=path, firefox_profile=firefox_profile)
		time.sleep(1)
		# disable ads
		self.driver.install_addon(os.path.abspath('uBlock0@raymondhill.net.xpi'), temporary=True)
		# maximize window
		self.driver.maximize_window()

		# movie details from user input
		self.name = name.lower()
		self.year = year

	def IMDB_Match(self):

		print('Searching...')

		self.driver.get('https://www.imdb.com/')
		time.sleep(0.5)
		self.driver.find_element_by_id('suggestion-search').send_keys(self.name + ' (' + self.year + ')')
		time.sleep(1.5)
		self.driver.find_element_by_id('suggestion-search-button').click()
		time.sleep(0.5)
		search_results = self.driver.find_elements_by_class_name('result_text')

		# setting an abritrary large edit
		num_edit = 999999
		# setting the index of possible match result
		result_index = 0
		# loop through the movie search results
		# use levenshtein distance to find the closest match
		for i in range(len(search_results)):
			ld_result = ld.levenshtein(self.name + ' (' + self.year + ')', search_results[i].text.lower())
			if ld_result < num_edit:
				result_index = i
				num_edit = ld_result

		try:
			# click on the link best matches user input
			self.driver.find_element_by_xpath('.//div[1]/div/div[2]/table/tbody/tr[' \
				+ str(result_index + 1) + ']/td[2]/a').click()
		except:
			# default first result
			self.driver.find_element_by_xpath('.//div[1]/div/div[2]/table/tbody/tr[2]/td[2]/a').click()

		time.sleep(0.5)
		# go to user reviews
		self.driver.find_elements_by_class_name('quicklink')[2].click()
		time.sleep(1)

		try:
			# click button to load 25 more reviews
			self.driver.find_element_by_id('load-more-trigger').click()
			time.sleep(1)
		except:
			pass

		self.IMDB_Scrape()

	def IMDB_Scrape(self):

		# holds the list of cleaned reviews
		review_list = []
		# holds all user ratings
		ratings = []

		# find all the review texts
		reviews = self.driver.find_elements_by_class_name('content')
		num_reviews = len(reviews)
		for k in range(num_reviews):
			# check if review is hidden
			if reviews[k].text == '':
				try:
					# expand the hidden (spoiler) reviews
					self.driver.find_element_by_xpath(".//div[1]/section/div[2]/div[2]/div[" \
						+ str(k + 1) + "]/div/div[1]/div[4]/div/div").click()
				except:
					pass

		time.sleep(0.5)

		print('Cleaning...')

		review_container = self.driver.find_elements_by_css_selector('.review-container')
		# gather and clean user reviews
		for i in range(num_reviews):
			review_list.append(cl.IMDB_Cleaner(review_container[i].text))
		
		# find all user ratings
		user_rating = self.driver.find_elements_by_class_name('rating-other-user-rating')

		# gather user ratings
		for j in range(len(user_rating)):
			ratings.append(float(user_rating[j].text.split('/')[0]))

		# close the firefox browser once it gets all the reviews
		self.driver.quit()

		print('Analyzing...')
		clf.Classifier(review_list).Categorize()

		print("User ratings (/10)")
		print("Mean: " + str(round(mean(ratings), 2)))
		print("Median: " + str(median(ratings)))
		print("Variance: " + str(round(variance(ratings), 2)))
		ratings.sort()
		print("Highest: " + str(ratings[-1]))
		print("Lowest: " + str(ratings[0]))
		print()
		# print the top 20 most common words
		print("Top 20 most common words and their counts:")
		print(Counter(' '.join(review_list).split()).most_common(20))
		print()

import scraper as sc

# helper function to ensure user enter a year
def Int_Check(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":

	print('Type quit() anywhere to exit.')
	movie = ''
	year = ''

	while movie != 'quit()' and year != 'quit()':

		# reset the strings for next movie
		year = ''
		movie = ''

		movie = str(input('What movie are you looking for? ').lower())
		if movie != 'quit()' and movie.strip() != '':

			while year != 'quit()' and year == '':
				year = str(input('What year was it released? '))

				if year != 'quit()' and year.strip() != '' and Int_Check(year.strip()):
					sc.IMDB(movie, year).IMDB_Match()
					
				elif year != 'quit()':
					print('Please enter a year.')

		elif movie != 'quit()':
			print('Please enter a movie title.')

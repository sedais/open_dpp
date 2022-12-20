from web_scraper_ifixit import get_the_content

df = get_the_content()
print(df.loc[15,'fact3'])


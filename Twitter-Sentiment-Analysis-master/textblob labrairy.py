for file in ['review', 'user']:
    print(file)
    json_file = yelp_dir / 'json' / f'yelp_academic_dataset_{file}.json'
    parquet_file = parquet_dir / f'{file}.parquet'

    data = json_file.read_text(encoding='utf-8')
    json_data = '[' + ','.join([l.strip()
                                for l in data.split('\n') if l.strip()]) + ']\n'
    data = json.loads(json_data)
    df = json_normalize(data)
    if file == 'review':
        df.date = pd.to_datetime(df.date)
        latest = df.date.max()
        df['year'] = df.date.dt.year
        df['month'] = df.date.dt.month
        df = df.drop(['date', 'business_id', 'review_id'], axis=1)
    if file == 'user':
        df.yelping_since = pd.to_datetime(df.yelping_since)
        df = (df.assign(member_yrs=lambda x: (latest - x.yelping_since)
                        .dt.days.div(365).astype(int))
              .drop(['elite', 'friends', 'name', 'yelping_since'], axis=1))
    df.dropna(how='all', axis=1).to_parquet(parquet_file, compression='gzip')
    try:
        pd.read_parquet(parquet_file, engine='pyarrow')
    except Exception as e:
        print(e)
        pd.read_parquet(parquet_file, engine='fastparquet')
        
user = pd.read_parquet(parquet_dir / 'user.parquet')
review = pd.read_parquet(parquet_dir / 'review.parquet', engine='fastparquet')
user_review = (review.merge(user, on='user_id', how='left', suffixes=['', '_user']).drop('user_id', axis=1))
user_review = user_review[user_review.stars > 0]
x=user_review['stars'].value_counts()
x=x.sort_index()
plt.figure(figsize=(10,6))
ax= sns.barplot(x.index, x.values, alpha=0.8)
plt.title("Star Rating Distribution")
plt.ylabel('count')
plt.xlabel('Star Ratings')
rects = ax.patches
labels = x.values
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')
plt.show();
fig, axes = plt.subplots(ncols=2, figsize=(14, 4))
user_review.year.value_counts().sort_index().plot.bar(title='Reviews per Year', ax=axes[0]);
sns.lineplot(x='year', y='stars', data=user_review, ax=axes[1])
axes[1].set_title('Stars per year');
user_review.member_yrs.value_counts()
review_sample = user_review.text.sample(1).iloc[0]
print(review_sample)
TextBlob(review_sample).sentiment
sample_reviews = user_review[['stars', 'text']].sample(1000000)
def detect_polarity(text):
    return TextBlob(text).sentiment.polarity
sample_reviews['polarity'] = sample_reviews.text.apply(detect_polarity)
sample_reviews.head()
num_bins = 50
plt.figure(figsize=(10,6))
n, bins, patches = plt.hist(sample_reviews.polarity, num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Polarity')
plt.ylabel('Count')
plt.title('Histogram of polarity')
plt.show();
plt.figure(figsize=(10,6))
sns.boxenplot(x='stars', y='polarity', data=sample_reviews)
plt.show();
sample_reviews[sample_reviews.polarity == -1].text.head()
sample_reviews[sample_reviews.stars == 1].text.head()
sample_reviews[(sample_reviews.stars == 5) & (sample_reviews.polarity == -1)].head(10)
sample_reviews[(sample_reviews.stars == 1) & (sample_reviews.polarity == 1)].head(10)

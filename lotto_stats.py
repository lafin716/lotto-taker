import pandas as pd
import utils as u
import matplotlib.pyplot as plt

from repo import lotto_repo


def make_df(list):
    df = pd.DataFrame.from_records(list, columns=['round', 'pick_date', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus', 'total_sell_amount', 'first_prize_winners', 'first_prize_amount', 'first_prize_each'])
    # 추첨일 날짜 형식으로 변환
    df['pick_date'] = pd.to_datetime(df['pick_date'].str.replace(' ', '')
                                     .str.replace('년', '-')
                                     .str.replace('월', '-')
                                     .str.replace('일', ''))
    df['year'] = df['pick_date'].dt.year
    df['year_quarter'] = df['pick_date'].dt.to_period('Q')
    return df

def get_prize_summary_yearly(df):
    result = df.groupby(by='year').mean()
    prizeFmt = lambda x: '{:.2f}억'.format(x / (10 ** 8))
    peopleFmt = lambda x: '{:,.2f}명'.format(x)

    result['total_sell_amount'] = result['total_sell_amount'].apply(prizeFmt)
    result['first_prize_amount'] = result['first_prize_amount'].apply(prizeFmt)
    result['first_prize_winners'] = result['first_prize_winners'].apply(peopleFmt)
    result['first_prize_each'] = result['first_prize_each'].apply(prizeFmt)
    result['max_prize_each'] = df.max()['first_prize_each']
    result['max_prize_each'] = result['max_prize_each'].apply(prizeFmt)

    print(result[['total_sell_amount', 'first_prize_amount', 'first_prize_winners', 'first_prize_each', 'max_prize_each']])

def get_prize_alltime_legend(df):
    min_prize_each_idx = df[df['first_prize_each'] > 0]['first_prize_each'].idxmin()
    min_prize_each = df.loc[min_prize_each_idx]
    min_prize_each_amount_full = u.format_price(min_prize_each['first_prize_each'])
    min_prize_each_amount_short = u.format_price(min_prize_each['first_prize_each'] / (10 ** 8), 2)
    max_prize_each_idx = df['first_prize_each'].idxmax()
    max_prize_each = df.loc[max_prize_each_idx]
    max_prize_each_amount_full = u.format_price(max_prize_each['first_prize_each'])
    max_prize_each_amount_short = u.format_price(max_prize_each['first_prize_each'] / (10 ** 8), 2)

    print('[역대 수령액 통계]')
    print('최대 수령 인원 : ' + str(max_prize_each['first_prize_winners']) + '명')
    print(f'최대 수령액 : {max_prize_each_amount_full}원 (약 {max_prize_each_amount_short}억)')
    print('최대 수령액 회차 : ' + str(max_prize_each['round']) + '회')
    print('최대 수령 추첨일 : ' + str(max_prize_each['pick_date']))
    print('최소 수령 인원 : ' + str(min_prize_each['first_prize_winners']) + '명')
    print(f'최소 수령액 : {min_prize_each_amount_full}원 (약 {min_prize_each_amount_short}억)')
    print('최소 수령액 회차 : ' + str(min_prize_each['round']) + '회')
    print('최소 수령 추첨일 : ' + str(min_prize_each['pick_date']))

def show_winners_year_quarter(df):
    quarterly_winners_max = df.groupby('year_quarter')['first_prize_winners'].max()
    quarterly_winners_min = df.groupby('year_quarter')['first_prize_winners'].min()

    # 그래프 사이즈 설정
    plt.figure(figsize=(15, 6))

    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    ax[0].bar(quarterly_winners_min.index.astype(str), quarterly_winners_min.values,
              color='blue', alpha=0.7)
    ax[0].set_title('Quarterly Lottery Winners (Min)')
    ax[0].set_ylabel('Number of Winners')

    ax[1].bar(quarterly_winners_max.index.astype(str), quarterly_winners_max.values,
              color='red', alpha=0.7)
    ax[1].set_title('Quarterly Lottery Winners (Max)')
    ax[1].set_xlabel('Quarter')
    ax[1].set_ylabel('Number of Winners')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    all_data = lotto_repo.get_all()
    df = make_df(all_data)
    print(df[['pick_date', 'year', 'year_quarter']])

    get_prize_summary_yearly(df)
    get_prize_alltime_legend(df)
    show_winners_year_quarter(df)


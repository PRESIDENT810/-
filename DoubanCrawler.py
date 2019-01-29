import requests
import expanddouban
import csv


def getMovieUrl(category=None, location=None):
    url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,"
    url += category
    url += ','
    url += location
    url += ','
    return url


class Movie:
    def __init__(self, name, rate, category, location, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.category = category
        self.location = location
        self.info_link = info_link
        self.cover_link = cover_link


def getMovies(category, location):
    url = getMovieUrl(category, location)
    response = requests.get(url)
    html = response.text
    html = expanddouban.getHtml(url)
    html_str = html.split('<div class="article">')
    html_str = html_str[1]
    html_str = html_str.split('<div class="aside">')
    html_str = html_str[0]
    html_str = html_str.split('href=')
    html_list = []

    for seg in html_str:
        if seg.startswith('"https:'):
            html_list.append(seg)

    movie_list = []

    for element in html_list:
        name = element.split('class="title">')[1]
        name = name.split('</span>')[0]

        rate = element.split('class="rate">')[1]
        rate = rate.split('</span>')[0]

        category = category

        location = location

        info_link = element.split(' class="item"')[0]

        cover_link = element.split('src=')[1]
        cover_link = cover_link.split(' alt=')[0]

        movie_list.append(Movie(name, rate, category, location, info_link, cover_link))

    write_csv(movie_list)
    return movie_list


def write_csv(movie_list):
    f = open('movies.csv', 'a', newline='', encoding='utf-8-sig')
    writer = csv.writer(f)
    for movie in movie_list:
        write_list = [movie.name, movie.rate, movie.location, movie.category, movie.info_link, movie.cover_link]
        writer.writerow(write_list)
        # for content in write_list:
        #     writer.writerow(content)
        print(movie.name, movie.rate, movie.location, movie.category, movie.info_link, movie.cover_link)

    f.close()


def stats(movie_list):
    location_dict = {}
    location_list = []
    for movie in movie_list:

        if movie.location not in location_list:
            location_list.append(movie.location)

        else:
            if movie.location not in location_dict:
                location_dict[movie.location] = 1
            else:
                location_dict[movie.location] += 1

    first_location = max(location_dict, key=location_dict.get)
    first_per = location_dict[first_location] / len(movie_list)
    first_per = str(first_per * 100) + '%'
    location_dict[first_location] = -1

    second_location = max(location_dict, key=location_dict.get)
    second_per = location_dict[second_location] / len(movie_list)
    second_per = str(second_per * 100) + '%'
    location_dict[second_location] = -1

    third_location = max(location_dict, key=location_dict.get)
    third_per = location_dict[third_location] / len(movie_list)
    third_per = str(third_per * 100) + '%'

    fhand = open('output.txt', 'w')
    fhand.write('The top three locations are: {}, {}, {}\n'.format(first_location, second_location, third_location))
    fhand.write('Their percentages are: {}, {}, {}\n'.format(first_per, second_per, third_per))


def main(category):
    movie_list = []
    for location in ['中国', '大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国', '意大利', '西班牙', '印度', '泰国', '俄罗斯', '伊朗',
                     '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']:
        movie_list += getMovies(category, location)

    stats(movie_list)


main("喜剧")
main("爱情")
main("历史")

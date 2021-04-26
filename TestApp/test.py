from selenium import webdriver
from ClothingStoreApp.models import Clothes, Size, Color, Category
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse


def createBooks():
    curSize = Size()
    curSize.sizeName = 'S'
    curSize.save()
    curSize = Size()
    curSize.sizeName = 'M'
    curSize.save()

    curColor = Color()
    curColor.colorName = 'черный'
    curColor.save()
    curColor = Color()
    curColor.colorName = 'белый'
    curColor.save()

    curCategory = Category()
    curCategory.categoryName = 'мужчины'
    curCategory.save()
    curCategory = Category()
    curCategory.categoryName = 'женщины'
    curCategory.save()


def createClothes():
    curClothes = Clothes()
    curClothes.clothesName = 'Товар для редактирования'
    curClothes.price = '111'
    curClothes.PK_Category = Category.objects.all().get(PK_Category=2)
    curClothes.PK_Size = Size.objects.all().get(PK_Size=2)
    curClothes.PK_Color = Color.objects.all().get(PK_Color=2)
    curClothes.description = 'Описание для редактирования'
    curClothes.save()


class TestApp(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('TestApp/chromedriver.exe')
        self.driver.get(self.live_server_url)

    def testAddingClothes(self):
        createBooks()

        print('Тест: Добавление товара')
        self.driver.get(self.live_server_url + '/products-administration/')

        countClothesStart = Clothes.objects.all().count()

        print('Кол-во товаров до добавления: ', countClothesStart)

        trueName = 'Тестовый товар'
        truePrice = '539'
        trueDescription = 'Описание тестового товара для мужчины размера S, цвет черный, цена 539'

        self.driver.find_element_by_xpath(
            '/html/body/section/div/div[1]/div/a').click()

        self.driver.find_element_by_xpath(
            '//*[@id="id_clothesName"]').send_keys(trueName)
        self.driver.find_element_by_xpath(
            "//*[@id='id_PK_Category']/option[2]").click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_PK_Size"]/option[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_PK_Color"]/option[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_price"]').send_keys(truePrice)
        self.driver.find_element_by_xpath(
            '//*[@id="id_description"]').send_keys(trueDescription)

        self.driver.find_element_by_xpath(
            '/html/body/section/div/div[2]/div/form/span[8]/button').click()

        countClothesEnd = Clothes.objects.all().count()
        print('Кол-во товаров до добавления: ', countClothesEnd)

        self.assertEquals(countClothesStart, countClothesEnd - 1)
        self.assertTrue(Clothes.objects.get(clothesName=trueName,
                                            price=truePrice, description=trueDescription) is not None)

    def testEditingClothes(self):
        createBooks()
        createClothes()

        print('Тест: Редактирование товара')

        self.driver.get(self.live_server_url + '/products-administration/')

        trueName = 'Измененное название тестового товара'
        truePrice = '978.00'
        trueDescription = 'Новое описание'

        self.driver.find_element_by_xpath(
            "/html/body/section/div/div[2]/div[1]/div/div/a[1]").click()

        self.driver.find_element_by_xpath('//*[@id="id_clothesName"]').clear()
        self.driver.find_element_by_xpath(
            '//*[@id="id_clothesName"]').send_keys(trueName)
        self.driver.find_element_by_xpath('//*[@id="id_price"]').clear()
        self.driver.find_element_by_xpath(
            '//*[@id="id_price"]').send_keys(truePrice)
        self.driver.find_element_by_xpath('//*[@id="id_description"]').clear()
        self.driver.find_element_by_xpath(
            '//*[@id="id_description"]').send_keys(trueDescription)

        self.driver.find_element_by_xpath(
            '/html/body/section/div/div[2]/div/form/span[8]/button').click()

        self.driver.find_element_by_xpath(
            '/html/body/section/div/div[2]/div[1]/div/a[1]').click()

        self.assertEquals(trueName, self.driver.find_element_by_xpath(
            '/html/body/section/div/div/div/div[2]/div[1]/div[1]').text)
        self.assertEquals(truePrice + "₽", self.driver.find_element_by_xpath(
            '/html/body/section/div/div/div/div[2]/div[1]/div[2]').text)
        self.assertEquals(trueDescription, self.driver.find_element_by_xpath(
            '/html/body/section/div/div/div/div[2]/div[2]/div').text)
        self.assertTrue(Clothes.objects.get(clothesName=trueName,
                                            price=truePrice, description=trueDescription) is not None)

    def testDeletingClothes(self):
        createBooks()
        createClothes()

        print('Тест: Удаление товара')

        countClothesStart = Clothes.objects.all().count()
        print('Кол-во товаров до удаления: ', countClothesStart)

        self.driver.get(self.live_server_url + '/products-administration/')

        trueName = self.driver.find_element_by_xpath(
            "/html/body/section/div/div[2]/div[1]/div/a[2]/div/div[1]").text
        truePrice = self.driver.find_element_by_xpath(
            "/html/body/section/div/div[2]/div[1]/div/a[2]/div/div[2]").text

        self.driver.find_element_by_xpath(
            "/html/body/section/div/div[2]/div[1]/div/div/a[2]").click()

        countClothesEnd = Clothes.objects.all().count()
        print('Кол-во товаров после удаления: ', countClothesEnd)

        self.assertEquals(countClothesStart, countClothesEnd + 1)
        self.assertTrue(Clothes.objects.all() is not True)

    def tearUp(self):
        self.driver.close()

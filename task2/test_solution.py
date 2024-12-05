import unittest
from unittest.mock import AsyncMock, Mock, patch

import aiohttp
from solution import count_animals_by_letter_on_page, get_page


class TestGetPage(unittest.IsolatedAsyncioTestCase):

    async def test_get_page(self):
        session = AsyncMock(spec=aiohttp.ClientSession)
        response_mock = AsyncMock()
        response_mock.status = 200
        response_mock.text.return_value = "test_get_page"
        session.get.return_value.__aenter__.return_value = response_mock
        result = await get_page(session, 'https://test.com')

        self.assertEqual(result, "test_get_page")


@patch('solution.BeautifulSoup')
class TestCountAnimalsByLetterOnPage(unittest.IsolatedAsyncioTestCase):

    async def test_count_animals_by_letter_on_page(self, mock_html):
        html = """ 
        <div class="mw-category mw-category-columns">
            <ul>
                <li><a href="#">Cat</a></li>
                <li><a href="#">Dog</a></li>
                <li><a href="#">Python</a></li>
            </ul> 
        </div>"""

        mock_soup = mock_html.return_value
        mock_div = mock_soup.find.return_value
        mock_uls = [Mock(), Mock()]
        mock_links = [
            [Mock(text='Cat'), Mock(text='Dog')],
            [Mock(text='Python')]
        ]
        mock_div.find_all.return_value = mock_uls
        for i, ul in enumerate(mock_uls):
            ul.find_all.return_value = mock_links[i]

        animals_count = {}
        await count_animals_by_letter_on_page(html, animals_count)

        self.assertEqual(animals_count['C'], 1)
        self.assertEqual(animals_count['D'], 1)
        self.assertEqual(animals_count['P'], 1)


if __name__ == '__main__':
    unittest.main()

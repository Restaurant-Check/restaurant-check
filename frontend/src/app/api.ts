import axios from 'axios';
import {Restaurant} from "@/app/page";

function generateRandomCoordinates(): [number, number] {
    const minLat = 48.0616; // Munich latitude bounds
    const maxLat = 48.2480;
    const minLon = 11.3600; // Munich longitude bounds
    const maxLon = 11.7223;

    const lat = (Math.random() * (maxLat - minLat) + minLat).toFixed(4);
    const lon = (Math.random() * (maxLon - minLon) + minLon).toFixed(4);
    return [Number(lat), Number(lon)];
}

function generateRandomRating(): number {
    return Math.random() * 5 + 1;
}

interface MenuItem {
    description: string;
    name: string;
    price: string;
}

interface MenuCategory {
    category: string;
    items: MenuItem[];
}

interface RestaurantData {
    menu: MenuCategory[];
    restaurant_name: string;
}

interface Highlight {
    category: string;
    description: string;
    name: string;
    price: string;
}

export const fetchRestaurants = async (query: string): Promise<Restaurant[]> => {
    try {
        const response = await axios.get('http://localhost:8000/query?query=' + query);

        const restaurantsData = response.data.restaurants;

        return restaurantsData.map((restaurant: { data: string, highlights: string[] }) => {
            const parsedData: RestaurantData = JSON.parse(restaurant.data);

            return {
                name: parsedData.restaurant_name,
                highlights: restaurant.highlights,
                coordinates: generateRandomCoordinates(),
                rating: generateRandomRating(),
                closingTime: '22:00',
                distance: '1.2km',
            };
        });
    } catch (error) {
        console.error('Error fetching restaurants:', error);
        throw error;
    }
};

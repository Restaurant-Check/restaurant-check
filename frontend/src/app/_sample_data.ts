function generateRandomCoordinates(): [number, number] {
    const minLat = 48.0616; // Munich latitude bounds
    const maxLat = 48.2480;
    const minLon = 11.3600; // Munich longitude bounds
    const maxLon = 11.7223;

    const lat = (Math.random() * (maxLat - minLat) + minLat).toFixed(4);
    const lon = (Math.random() * (maxLon - minLon) + minLon).toFixed(4);
    return [Number(lat), Number(lon)];
}

export const SampleData = [
    {
        name: 'Restaurant 1',
        rating: 4.5,
        distance: '1.2km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates(),
    },
    {
        name: 'Restaurant 2',
        rating: 4.2,
        distance: '2.1km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates(),
    },
    {
        name: 'Restaurant 3',
        rating: 4.8,
        distance: '0.5km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates(),
    },
    {
        name: 'Restaurant 4',
        rating: 4.1,
        distance: '3.2km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates(),
    },
    {
        name: 'Restaurant 5',
        rating: 4.9,
        distance: '0.3km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates()
    },
    {
        name: 'Restaurant 6',
        rating: 4.6,
        distance: '2.5km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates()
    },
    {
        name: 'Restaurant 7',
        rating: 4.3,
        distance: '1.7km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates()
    },
    {
        name: 'Restaurant 8',
        rating: 4.7,
        distance: '0.8km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates()
    },
    {
        name: 'Restaurant 9',
        rating: 4.4,
        distance: '2.9km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates()
    },
    {
        name: 'Restaurant 10',
        rating: 4.0,
        distance: '3.9km',
        closingTime: '22:00',
        top3MenuItems: ['Salads: Insalata di Cetrioli Cucumber salad | 7.00', 'Meat Dishes: Cotoletta alla Primavera Breaded turkey cutlet with arugula, tomatoes, and garlic | 23.50',
            'Meat Dishes: Tagliata alla griglia Sliced grilled beef tenderloin on arugula with shaved Parmesan | 26.50'],
        coordinates: generateRandomCoordinates()
    },
];
import '@mantine/core/styles.css';
import './page.css';
import 'leaflet/dist/leaflet.css';

import {ColorSchemeScript, MantineProvider} from '@mantine/core';
import React from "react";
import StyledComponentsRegistry from "@/app/_lib/registry";

export const metadata = {
    title: 'Restaurant Check',
    description: '',
};

export default function RootLayout({
                                       children,
                                   }: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
        <head>
            <ColorSchemeScript/><title>Restaurant Check</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
                  integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
                  crossOrigin=""/>
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
                    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
                    crossOrigin=""></script>
        </head>
        <body>
        <StyledComponentsRegistry>
            <MantineProvider defaultColorScheme={'dark'}>{children}</MantineProvider>
        </StyledComponentsRegistry>
        </body>
        </html>
    );
}
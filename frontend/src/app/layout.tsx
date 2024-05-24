import '@mantine/core/styles.css';
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
            <ColorSchemeScript/>
        </head>
        <body>
        <StyledComponentsRegistry>
            <MantineProvider defaultColorScheme={'dark'}>{children}</MantineProvider>
        </StyledComponentsRegistry>
        </body>
        </html>
    );
}
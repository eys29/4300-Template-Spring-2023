import React from 'react';
import { Container } from '@mui/material';

const Layout =({children}) =>{
    return(
        <div>
            <Container maxWidth="lg">{children}</Container>
        </div>
    )
}

export default Layout;
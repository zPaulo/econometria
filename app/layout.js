import './globals.css'

export const metadata = {
  title: 'Econometria 2 - Plataforma Interativa',
  description: 'Aprenda séries temporais, modelos ARMA/ARIMA e econometria de forma fácil.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  )
}

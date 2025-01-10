import express from 'express'
import { NFTController } from './controllers/nftController'

const app = express()
const nftController = new NFTController()

app.use(express.json())

app.post('/api/nft/create', (req, res) => nftController.createNFT(req, res))
app.get('/api/nft/owner/:owner', (req, res) => nftController.fetchByOwner(req, res))

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
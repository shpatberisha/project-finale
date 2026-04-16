export interface Sneaker {
  id: number
  name: string
  brand_id: number
  product_link: string | null
  categories: string[]
  price: number | null
  release_year: number | null
  colorway: string | null
}

export interface Brand {
  id: number
  name: string
}

export interface SneakerCreate {
  name: string
  brand_id: number
  product_link?: string
  categories: string[]
  price?: number
  release_year?: number
  colorway?: string
}

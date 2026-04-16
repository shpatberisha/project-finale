const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export const fetcher = async (url: string) => {
  const res = await fetch(`${API_BASE_URL}${url}`)
  if (!res.ok) {
    throw new Error("Failed to fetch data")
  }
  return res.json()
}

export async function createSneaker(data: {
  name: string
  brand_id: number
  product_link?: string
  categories: string[]
  price?: number
  release_year?: number
  colorway?: string
}, apiKey: string) {
  const res = await fetch(`${API_BASE_URL}/api/sneakers/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
    },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    throw new Error("Failed to create sneaker")
  }
  return res.json()
}

export async function updateSneaker(
  id: number,
  data: {
    name: string
    brand_id: number
    product_link?: string
    categories: string[]
    price?: number
    release_year?: number
    colorway?: string
  },
  apiKey: string
) {
  const res = await fetch(`${API_BASE_URL}/api/sneakers/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
    },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    throw new Error("Failed to update sneaker")
  }
  return res.json()
}

export async function deleteSneaker(id: number, apiKey: string) {
  const res = await fetch(`${API_BASE_URL}/api/sneakers/${id}`, {
    method: "DELETE",
    headers: {
      "x-api-key": apiKey,
    },
  })
  if (!res.ok) {
    throw new Error("Failed to delete sneaker")
  }
  return res.json()
}

export async function createBrand(name: string, apiKey: string) {
  const res = await fetch(`${API_BASE_URL}/api/brands/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
    },
    body: JSON.stringify({ name }),
  })
  if (!res.ok) {
    throw new Error("Failed to create brand")
  }
  return res.json()
}

export async function deleteBrand(id: number, apiKey: string) {
  const res = await fetch(`${API_BASE_URL}/api/brands/${id}`, {
    method: "DELETE",
    headers: {
      "x-api-key": apiKey,
    },
  })
  if (!res.ok) {
    throw new Error("Failed to delete brand")
  }
  return res.json()
}

export { API_BASE_URL }

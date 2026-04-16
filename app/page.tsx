import { Header } from "@/components/header"
import { Sidebar } from "@/components/sidebar"
import { SneakerGrid } from "@/components/sneaker-grid"

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <SneakerGrid />
        </main>
      </div>
    </div>
  )
}

import { NextRequest, NextResponse } from 'next/server'
import { getDashboardStats, getAllLeads, getAllClients } from '@/lib/database'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const type = searchParams.get('type')

    switch (type) {
      case 'stats':
        const stats = await getDashboardStats()
        return NextResponse.json({
          success: true,
          data: stats
        })

      case 'leads':
        const leads = await getAllLeads()
        return NextResponse.json({
          success: true,
          data: leads
        })

      case 'clients':
        const clients = await getAllClients()
        return NextResponse.json({
          success: true,
          data: clients
        })

      default:
        // Return comprehensive dashboard data
        const [dashboardStats, recentLeads, recentClients] = await Promise.all([
          getDashboardStats(),
          getAllLeads(),
          getAllClients()
        ])

        return NextResponse.json({
          success: true,
          data: {
            stats: dashboardStats,
            recentLeads: recentLeads?.slice(0, 10) || [], // Latest 10 leads
            recentClients: recentClients?.slice(0, 10) || [] // Latest 10 clients
          }
        })
    }

  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: 'Failed to fetch dashboard data' 
      },
      { status: 500 }
    )
  }
}
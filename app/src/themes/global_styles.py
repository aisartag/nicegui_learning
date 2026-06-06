from nicegui import ui


def add_tailwind_styles():
	ui.add_head_html("""
        <style type="text/tailwindcss">
        @layer components {
            .btn-indigo { 
                @apply text-white! bg-indigo-600! dark:bg-indigo-500!; 
            }
            .card-custom { 
                @apply bg-white! bg-slate-100! text-slate-800! dark:bg-slate-900!  dark:text-blue-200!; 
            }
            .input-custom { 
                @apply bg-gray-50! dark:bg-slate-900! text-gray-900! dark:text-white!; 
            }
        }
    </style>
        """)

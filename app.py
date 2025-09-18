import streamlit as st
import pandas as pd
import time
from scraper import GradeScraper
import threading
import queue

# Configure page
st.set_page_config(
    page_title="Egyptian Education Grades Scraper",
    page_icon="📊",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'scraping_active' not in st.session_state:
        st.session_state.scraping_active = False
    if 'scraping_complete' not in st.session_state:
        st.session_state.scraping_complete = False
    if 'results_data' not in st.session_state:
        st.session_state.results_data = []
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'current_seat' not in st.session_state:
        st.session_state.current_seat = None
    if 'total_seats' not in st.session_state:
        st.session_state.total_seats = 0
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    if 'scraper_thread' not in st.session_state:
        st.session_state.scraper_thread = None
    if 'result_queue' not in st.session_state:
        st.session_state.result_queue = queue.Queue()
    if 'stop_event' not in st.session_state:
        st.session_state.stop_event = None

def scraping_worker(start_seat, end_seat, result_queue, demo_mode=False, stop_event=None):
    """Worker function for scraping in a separate thread"""
    try:
        scraper = GradeScraper(demo_mode=demo_mode)
        results = []
        
        # Get token first
        if not scraper.initialize_session():
            if demo_mode:
                result_queue.put(('error', 'Demo mode initialization failed'))
            else:
                result_queue.put(('error', 'Failed to connect to nategafany.emis.gov.eg. This could be due to network restrictions or the website being unavailable.'))
            return
        
        total_seats = end_seat - start_seat + 1
        
        for i, seat_number in enumerate(range(start_seat, end_seat + 1)):
            # Check if we should stop
            if stop_event and stop_event.is_set():
                break
                
            # Update progress
            progress = (i + 1) / total_seats
            result_queue.put(('progress', {
                'progress': progress,
                'current_seat': seat_number,
                'completed': i + 1,
                'total': total_seats
            }))
            
            # Scrape grades for current seat
            result = scraper.scrape_grades(seat_number)
            results.append(result)
            result_queue.put(('result', result))
            
            # Small delay to prevent overwhelming the server
            delay = 0.1 if demo_mode else 0.5
            time.sleep(delay)
        
        # Signal completion
        result_queue.put(('complete', results))
        
    except Exception as e:
        result_queue.put(('error', str(e)))

def main():
    st.title("📊 Egyptian Education Grades Scraper")
    st.markdown("---")
    
    # Always initialize session state first
    initialize_session_state()
    
    # Control panel
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Scraping Configuration")
        
        # Demo mode toggle
        demo_mode = st.checkbox(
            "Demo Mode", 
            value=True,
            help="Use demo mode with simulated data when the target website is not accessible",
            disabled=st.session_state.scraping_active
        )
        
        if demo_mode:
            st.info("🔬 Demo mode is enabled. The app will use simulated Egyptian grade data for testing.")
        else:
            st.warning("⚠️ Live mode: Attempting to connect to nategafany.emis.gov.eg (may fail due to network restrictions)")
        
        # Range selection
        start_seat = st.number_input(
            "Start Seat Number", 
            min_value=1, 
            value=3025301, 
            step=1,
            disabled=st.session_state.scraping_active
        )
        
        end_seat = st.number_input(
            "End Seat Number", 
            min_value=start_seat, 
            value=3025399, 
            step=1,
            disabled=st.session_state.scraping_active
        )
        
        total_seats = end_seat - start_seat + 1
        st.info(f"Total seats to scrape: {total_seats}")
    
    with col2:
        st.subheader("Actions")
        
        if not st.session_state.scraping_active:
            if st.button("🚀 Start Scraping", type="primary", use_container_width=True):
                # Reset state
                st.session_state.scraping_active = True
                st.session_state.scraping_complete = False
                st.session_state.results_data = []
                st.session_state.progress = 0
                st.session_state.current_seat = None
                st.session_state.total_seats = total_seats
                st.session_state.error_message = None
                
                # Clear the queue
                while not st.session_state.result_queue.empty():
                    st.session_state.result_queue.get()
                
                # Create stop event for thread communication
                st.session_state.stop_event = threading.Event()
                
                # Start scraping thread
                st.session_state.scraper_thread = threading.Thread(
                    target=scraping_worker,
                    args=(start_seat, end_seat, st.session_state.result_queue, demo_mode, st.session_state.stop_event)
                )
                st.session_state.scraper_thread.start()
                st.rerun()
        else:
            if st.button("⏹️ Stop Scraping", type="secondary", use_container_width=True):
                st.session_state.scraping_active = False
                if st.session_state.stop_event:
                    st.session_state.stop_event.set()
                st.rerun()
    
    # Process queue messages
    while not st.session_state.result_queue.empty():
        try:
            message_type, data = st.session_state.result_queue.get_nowait()
            
            if message_type == 'progress':
                st.session_state.progress = data['progress']
                st.session_state.current_seat = data['current_seat']
            elif message_type == 'result':
                st.session_state.results_data.append(data)
            elif message_type == 'complete':
                st.session_state.scraping_active = False
                st.session_state.scraping_complete = True
                st.session_state.progress = 1.0
            elif message_type == 'error':
                st.session_state.scraping_active = False
                st.session_state.error_message = data
        except queue.Empty:
            break
    
    # Progress display
    if st.session_state.scraping_active or st.session_state.scraping_complete:
        st.markdown("---")
        st.subheader("📈 Scraping Progress")
        
        # Progress bar
        progress_bar = st.progress(st.session_state.progress)
        
        # Status information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.current_seat:
                st.metric("Current Seat", st.session_state.current_seat)
        
        with col2:
            completed = len(st.session_state.results_data)
            st.metric("Completed", f"{completed}/{st.session_state.total_seats}")
        
        with col3:
            if st.session_state.scraping_complete:
                st.success("✅ Scraping Complete!")
            elif st.session_state.scraping_active:
                st.info("🔄 Scraping in progress...")
            
        # Auto-refresh while scraping
        if st.session_state.scraping_active:
            time.sleep(1)
            st.rerun()
    
    # Error display
    if st.session_state.error_message:
        st.error(f"❌ Error: {st.session_state.error_message}")
    
    # Results display
    if st.session_state.results_data:
        st.markdown("---")
        st.subheader("📋 Scraping Results")
        
        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.results_data)
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            if 'Error' in df.columns:
                error_count = len(df[(df['Error'].notna()) & (df['Error'] != '')])
            else:
                error_count = 0
            st.metric("Errors", error_count)
        with col3:
            success_count = len(df) - error_count
            st.metric("Successful", success_count)
        
        # Filtering options
        st.subheader("🔍 Filter Options")
        col1, col2 = st.columns(2)
        
        with col1:
            show_errors_only = st.checkbox("Show errors only")
            show_successful_only = st.checkbox("Show successful only")
        
        with col2:
            if 'Seat Number' in df.columns:
                seat_filter = st.text_input("Filter by seat number (partial match)")
        
        # Apply filters
        filtered_df = df.copy()
        
        if show_errors_only:
            has_error = filtered_df['Error'].notna() & (filtered_df['Error'] != '') if 'Error' in filtered_df.columns else pd.Series([False] * len(filtered_df))
            filtered_df = filtered_df[has_error]
        elif show_successful_only:
            no_error = filtered_df['Error'].isna() | (filtered_df['Error'] == '') if 'Error' in filtered_df.columns else pd.Series([True] * len(filtered_df))
            filtered_df = filtered_df[no_error]
        
        seat_filter = locals().get('seat_filter', '')
        if seat_filter:
            if 'Seat Number' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Seat Number'].astype(str).str.contains(seat_filter, na=False)]
        
        # Display table
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        if not filtered_df.empty:
            # Convert to CSV with proper UTF-8 BOM encoding for Excel compatibility
            csv_data = filtered_df.to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name=f"grades_{start_seat}_{end_seat}.csv",
                mime="text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    main()

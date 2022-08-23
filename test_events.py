def test_unauthorized_access(self):
        """When the user is logged out, can they access routes manually?"""
        with self.client as c:           
            contact=c.get('/contact', follow_redirects=True)
            contact_html=contact.get_data(as_text=True)
            self.assertIn('Please log in', contact_html)
            self.assertNotIn('Email', contact_html)

            docs=c.get('/docs', follow_redirects=True)
            docs_html=docs.get_data(as_text=True)
            self.assertIn('Please log in', docs_html)
            self.assertNotIn('Download', docs_html)

            photos=c.get('/photos', follow_redirects=True)
            photos_html=photos.get_data(as_text=True)
            self.assertIn('Please log in', photos_html)
            self.assertNotIn('Photos', photos_html)

            edit=c.get('/edit_profile', follow_redirects=True)
            edit_html=edit.get_data(as_text=True)
            self.assertIn('Please log in', edit_html)
            self.assertNotIn('Edit Your Profile.', edit_html)

            events=c.get('/events', follow_redirects=True)
            events_html=events.get_data(as_text=True)
            self.assertIn('Please log in', events_html)
            self.assertNotIn('Upcoming', events_html)
    
            # add_event=c.get('/add_event', follow_redirects=True)
            # add_event_html=add_event.get_data(as_text=True)
            # self.assertIn('Not authorized', add_event_html)
            # self.assertNotIn('Upcoming', add_event_html)
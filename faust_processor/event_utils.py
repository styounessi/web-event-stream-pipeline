class EventEnrichment:
    @staticmethod
    def categorize_utm_source(utm_source):
        '''
        Categorizes UTM (Urchin Tracking Modules) sources
        into higher level groupings.

        Args:
            utm_source (str): UTM source value.

        Returns:
            str: Assigned category of the UTM source.
        '''
        if utm_source in ['google', 'bing']:
            return 'search_engine'
        elif utm_source in ['facebook', 'instagram']:
            return 'social_media'
        elif utm_source in ['mailchimp']:
            return 'email_marketing'
        else:
            return 'other/unknown'
        
    
    @staticmethod
    def extract_email_domain(user_custom_id):
        '''
        Extracts the email domain from the user_custom_id.

        Args:
            user_custom_id (str): User's email address based custom_id.

        Returns:
            str: Email domain extracted from the user_custom_id.
        '''
        if '@' in user_custom_id:
            _, email_domain = user_custom_id.split('@')
            return email_domain
        else:
            return 'n/a'

"""
Comprehensive System Integration Test Runner
Executes all integration tests and generates system status reports.
"""

import sys
import os
from pathlib import Path

# Add system path for imports
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_system_integration import enhanced_integration
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system_integration_tests.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Run comprehensive system integration tests"""
    logger.info("=" * 80)
    logger.info("STARTING ENHANCED SYSTEM INTEGRATION TESTS")
    logger.info("=" * 80)
    
    try:
        # Generate comprehensive system status report
        logger.info("Generating comprehensive system status report...")
        status_report = enhanced_integration.generate_system_status_report()
        
        logger.info("System status report generated successfully")
        logger.info("=" * 80)
        
        # Print key results to console
        print("\n" + "=" * 80)
        print("SYSTEM INTEGRATION TEST RESULTS")
        print("=" * 80)
        print(status_report)
        print("=" * 80)
        
        logger.info("System integration tests completed successfully")
        
    except Exception as e:
        logger.error(f"System integration tests failed: {str(e)}")
        print(f"\nERROR: System integration tests failed - {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)